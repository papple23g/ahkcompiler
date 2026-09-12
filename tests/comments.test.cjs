const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');

function fixture(protocol = 'https:') {
    let click, timeout;
    const scripts = [];
    const button = {addEventListener: (_, callback) => {click = callback;}};
    const status = {};
    const fallback = {};
    const events = {};
    const frame = {tagName: 'IFRAME'};
    const thread = {contains: element => element === frame};
    const window = {location: {protocol}, addEventListener: (name, handler) => {events[name] = handler;}};
    const context = {
        window,
        document: {
            activeElement: frame,
            hasFocus: () => false,
            getElementById: id => ({'comments-load': button, 'comments-status': status, 'comments-fallback': fallback, 'disqus_thread': thread})[id],
            createElement: () => ({remove() {this.removed = true;}}),
            head: {appendChild: script => scripts.push(script)},
        },
        setTimeout: callback => {timeout = callback; return 1;},
        clearTimeout: () => {timeout = null;},
    };
    vm.runInNewContext(fs.readFileSync('static/comments.js', 'utf8'), context);
    return {window, button, status, fallback, scripts, events, document: context.document, click: () => click(), expire: () => timeout()};
}

test('automatically loads the verified legacy thread, keeping controls hidden until failure', () => {
    const app = fixture();
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
});

test('return from comments refreshes once and a failed refresh still permits retry', () => {
    const app = fixture();
    const config = {page: {}, callbacks: {}};
    app.window.disqus_config.call(config);
    config.callbacks.onReady[0]();
    let resets = 0;
    app.window.DISQUS = {reset: () => {resets++;}};
    app.events.blur();
    app.expire();
    app.events.focus();
    assert.equal(resets, 1);
    app.expire();
    assert.equal(app.button.hidden, false);
    config.callbacks.onReady[0]();
    app.events.blur();
    app.events.focus();
    assert.equal(resets, 1);
});

test('ordinary focus, focus within the page and identified users do not reload', () => {
    const app = fixture();
    const config = {page: {}, callbacks: {}};
    app.window.disqus_config.call(config);
    config.callbacks.onReady[0]();
    let resets = 0;
    app.window.DISQUS = {reset: () => {resets++;}};
    app.events.focus();
    app.document.hasFocus = () => true;
    app.events.blur();
    app.expire();
    app.events.focus();
    config.callbacks.onIdentify[0]('123');
    app.document.hasFocus = () => false;
    app.events.blur();
    app.events.focus();
    assert.equal(resets, 0);
});
