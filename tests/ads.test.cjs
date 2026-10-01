const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');

function fixture(options = {}) {
    const config = {hostname: 'papple23g-ahkcompiler.herokuapp.com', protocol: 'https:',
        pathname: '/ahkblockly', slot: '1234567890', width: 1366, frameWidth: 390,
        ready: true, ...options};
    const observers = [];
    const resizeObservers = [];
    const scripts = [];
    const timers = new Map();
    const timeoutStarts = [];
    const region = {hidden: true, dataset: {adSlot: config.slot},
        appendChild: ad => {region.ad = ad;}};
    const preview = {hidden: true};
    const frame = {getBoundingClientRect: () => ({width: config.frameWidth})};
    const container = {};
    const column = {querySelector: selector => selector === 'iframe' ? frame : null,
        insertBefore: element => {column.region = element;}};
    let columnReady = config.ready;
    class Observer {
        constructor(callback) {this.callback = callback; observers.push(this);}
        observe(target) {this.target = target; this.connected = true;}
        disconnect() {this.connected = false;}
        notify() {if (this.connected) this.callback();}
    }
    class Resize extends Observer {
        constructor(callback) {super(callback); resizeObservers.push(this);}
    }
    const window = {location: config, innerWidth: config.width};
    if (config.pushFailure) window.adsbygoogle = {push() {throw new Error('blocked');}};
    const document = {
        getElementById: id => ({'ahk-ad': region, 'ahk-ad-preview': preview,
            ahk_help_column: columnReady ? column : null, div_subMainPage: container})[id],
        createElement: () => ({dataset: {}, style: {},
            getAttribute(name) {return name === 'data-ad-status' ? this.status : null;}}),
        head: {appendChild: script => scripts.push(script)},
    };
    vm.runInNewContext(fs.readFileSync('static/ahk_ads.js', 'utf8'), {
        window, document, MutationObserver: Observer, ResizeObserver: Resize,
        setTimeout: (callback, delay) => {
            const id = timeoutStarts.push(delay);
            timers.set(id, {callback, delay});
            return id;
        },
        clearTimeout: id => timers.delete(id),
    });
    return {window, config, region, preview, column, frame, observers, resizeObservers,
        scripts, timers, timeoutStarts,
        ready() {
            columnReady = true;
            observers.find(observer => observer.target === container)?.notify();
        },
        status(value) {
            region.ad.status = value;
            observers.find(observer => observer.target === region.ad).notify();
        },
        resize(frameWidth, viewportWidth = config.width) {
            window.innerWidth = viewportWidth;
            config.frameWidth = frameWidth;
            resizeObservers.forEach(observer => observer.notify());
        },
        expire() {timers.values().next().value.callback();},
    };
}

test('localhost previews the fixed slot without a Google request even with a configured ID', () => {
    for (const hostname of ['127.0.0.1', 'localhost', '[::1]']) {
        const app = fixture({hostname, protocol: 'http:', width: 320, frameWidth: 300});
        assert.equal(app.region.hidden, false);
        assert.equal(app.preview.hidden, false);
        assert.equal(app.column.region, app.region);
        assert.equal(app.scripts.length, 0);
        assert.equal(app.region.ad, undefined);
        app.resize(299);
        assert.equal(app.region.hidden, true);
        app.resize(300);
        assert.equal(app.region.hidden, false);
        assert.equal(app.scripts.length, 0);
    }
});

test('only an eligible production host, path, HTTPS and slot may request ads', () => {
    for (const options of [{slot: ''}, {slot: '１２３'}, {hostname: 'example.com'},
        {protocol: 'http:'}, {protocol: 'file:'}, {pathname: '/faq'}]) {
        const app = fixture(options);
        assert.equal(app.scripts.length, 0, JSON.stringify(options));
        assert.equal(app.region.hidden, true);
    }
});

test('300px of actual iframe width permits ads, while 299px waits for enough room', () => {
    const app = fixture({width: 320, frameWidth: 299});
    assert.equal(app.region.hidden, true);
    assert.equal(app.scripts.length, 0);
    assert.equal(app.region.ad, undefined);
    assert.equal(app.timeoutStarts.length, 0);
    app.resize(300);
    assert.equal(app.region.hidden, false);
    assert.equal(app.scripts.length, 1);
    assert.equal(app.resizeObservers[0].target, app.frame);
    app.scripts[0].onload();
    app.resize(299);
    app.resize(300);
    assert.equal(app.scripts.length, 1);
    assert.equal(app.window.adsbygoogle.length, 1);
    assert.deepEqual(app.timeoutStarts, [20000]);
    assert.equal(fixture({width: 375, frameWidth: 300}).scripts.length, 1);
});

test('waits for Brython, initializes once, and never refreshes on resize or later DOM changes', () => {
    const app = fixture({ready: false});
    assert.equal(app.scripts.length, 0);
    app.ready();
    app.ready();
    assert.equal(app.scripts.length, 1);
    assert.equal(app.region.ad.dataset.adClient, 'ca-pub-3626951597834728');
    assert.equal(app.region.ad.style.cssText, 'display:inline-block;width:300px;height:250px');
    app.scripts[0].onload();
    assert.equal(app.window.adsbygoogle.length, 1);
    app.resize(299, 320);
    assert.equal(app.region.hidden, true);
    app.resize(390, 1366);
    assert.equal(app.region.hidden, false);
    assert.equal(app.scripts.length, 1);
    assert.equal(app.window.adsbygoogle.length, 1);
});

test('narrowing during script loading defers the single push without resetting timeout', () => {
    const app = fixture();
    const ad = app.region.ad;
    app.resize(299);
    app.scripts[0].onload();
    assert.equal(app.region.hidden, true);
    assert.equal(app.window.adsbygoogle, undefined);
    assert.equal(app.timers.size, 1);
    app.resize(300);
    assert.equal(app.region.hidden, false);
    assert.equal(app.region.ad, ad);
    assert.equal(app.window.adsbygoogle.length, 1);
    app.resize(299);
    app.resize(390);
    assert.equal(app.scripts.length, 1);
    assert.equal(app.window.adsbygoogle.length, 1);
    assert.deepEqual(app.timeoutStarts, [20000]);
});

test('no fill, blocked scripts, timeout and push failure remain hidden after widening', () => {
    for (const failure of ['unfilled', 'blocked', 'timeout', 'push']) {
        const app = fixture({pushFailure: failure === 'push'});
        const ad = app.region.ad;
        if (failure === 'blocked') app.scripts[0].onerror();
        else if (failure === 'timeout') app.expire();
        else {
            app.scripts[0].onload();
            if (failure === 'unfilled') app.status('unfilled');
        }
        assert.equal(app.region.hidden, true, failure);
        assert.equal(app.timers.size, 0, failure);
        app.resize(299);
        app.resize(390);
        app.scripts[0].onload();
        assert.equal(app.region.hidden, true, failure);
        assert.equal(app.region.ad, ad, failure);
        assert.equal(app.scripts.length, 1, failure);
        assert.deepEqual(app.timeoutStarts, [20000], failure);
        if (failure === 'blocked' || failure === 'timeout') {
            assert.equal(app.window.adsbygoogle, undefined, failure);
        }
    }
});

test('a filled slot restores the same DOM after narrowing without a refresh timer', () => {
    const app = fixture();
    const ad = app.region.ad;
    app.scripts[0].onload();
    app.status('filled');
    assert.equal(app.region.hidden, false);
    assert.equal(app.timers.size, 0);
    app.resize(299);
    assert.equal(app.region.hidden, true);
    app.resize(300);
    assert.equal(app.region.hidden, false);
    assert.equal(app.region.ad, ad);
    assert.equal(app.scripts.length, 1);
    assert.equal(app.window.adsbygoogle.length, 1);
    assert.deepEqual(app.timeoutStarts, [20000]);
});
