const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');

function fixture(protocol = 'https:', readyState = 'loading') {
    let click;
    let nextTimer = 0;
    const timers = new Map();
    const events = {};
    const scripts = [];
    const button = {addEventListener: (_, callback) => {click = callback;}};
    const status = {};
    const fallback = {};
    const window = {location: {protocol}, addEventListener: (name, callback) => {events[name] = callback;}};
    const context = {
        window,
        document: {
            readyState,
            getElementById: id => ({'comments-load': button, 'comments-status': status, 'comments-fallback': fallback})[id],
            createElement: () => ({remove() {this.removed = true;}}),
            head: {appendChild: script => scripts.push(script)},
        },
        setTimeout: (callback, delay) => {const id = ++nextTimer; timers.set(id, {callback, delay}); return id;},
        clearTimeout: id => {timers.delete(id);},
    };
    vm.runInNewContext(fs.readFileSync('static/comments.js', 'utf8'), context);
    function runTimer(delay) {
        const entry = [...timers].find(([, timer]) => timer.delay === delay);
        assert.ok(entry, `expected a ${delay}ms timer`);
        timers.delete(entry[0]);
        entry[1].callback();
    }
    return {window, button, status, fallback, scripts, timers,
        pageLoaded: () => events.load?.(),
        start: () => {events.load?.(); runTimer(0);},
        click: () => click(), expire: () => runTimer(20000)};
}

test('automatically loads the verified legacy thread, keeping controls hidden until failure', () => {
    const app = fixture();
    app.start();
    assert.equal(app.scripts.length, 1);
    assert.equal(app.button.hidden, true);
    assert.equal(app.fallback.hidden, true);
    assert.equal(app.scripts[0].src, 'https://ahkcompiler.disqus.com/embed.js');
    const config = {page: {}, callbacks: {}};
    app.window.disqus_config.call(config);
    assert.equal(config.page.identifier, 'r1RuM08tB');
    assert.equal(config.page.url, 'https://hackmd.io/%40papple23g/r1RuM08tB');
    config.callbacks.onReady[0]();
    assert.equal(app.button.hidden, true);
    assert.equal(app.status.textContent, '');
});

test('script failure permits retry and removes the failed script', () => {
    const app = fixture();
    app.start();
    app.scripts[0].onerror();
    assert.equal(app.button.hidden, false);
    assert.equal(app.fallback.hidden, false);
    assert.equal(app.button.disabled, false);
    assert.match(app.status.textContent, /尚未載入/);
    app.click();
    assert.equal(app.scripts[0].removed, true);
    assert.equal(app.scripts.length, 2);
});

test('iframe timeout retries through Disqus reset without another embed script', () => {
    const app = fixture();
    app.start();
    app.expire();
    assert.equal(app.button.disabled, false);
    let reset;
    app.window.DISQUS = {reset: options => {reset = options;}};
    app.click();
    assert.equal(reset.reload, true);
    assert.equal(reset.config, app.window.disqus_config);
    assert.equal(app.scripts.length, 1);
});

test('file URLs never attach a loader', () => {
    const app = fixture('file:');
    assert.equal(app.window.disqus_config, undefined);
    assert.equal(app.scripts.length, 0);
    assert.equal(app.timers.size, 0);
});

test('waits for page load and a later task; timeout begins only with the request', () => {
    const app = fixture();
    assert.equal(app.scripts.length, 0);
    assert.equal(app.timers.size, 0);
    app.pageLoaded();
    assert.equal(app.scripts.length, 0);
    assert.deepEqual([...app.timers.values()].map(t => t.delay), [0]);
    app.start();
    assert.equal(app.scripts.length, 1);
    assert.deepEqual([...app.timers.values()].map(t => t.delay), [20000]);
    app.pageLoaded();
    assert.equal(app.scripts.length, 1);
    assert.deepEqual([...app.timers.values()].map(t => t.delay), [20000]);
});

test('a script attached after page load still schedules automatic loading', () => {
    const app = fixture('https:', 'complete');
    assert.equal(app.scripts.length, 0);
    app.start();
    assert.equal(app.scripts.length, 1);
});
