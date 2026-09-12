const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');

function fixture(protocol = 'https:') {
    let click, timeout;
    const scripts = [];
    const button = {addEventListener: (_, callback) => {click = callback;}};
    const status = {};
    const window = {location: {protocol}};
    const context = {
        window,
        document: {
            getElementById: id => id === 'comments-load' ? button : status,
            createElement: () => ({remove() {this.removed = true;}}),
            head: {appendChild: script => scripts.push(script)},
        },
        setTimeout: callback => {timeout = callback; return 1;},
        clearTimeout: () => {timeout = null;},
    };
    vm.runInNewContext(fs.readFileSync('static/comments.js', 'utf8'), context);
    return {window, button, status, scripts, click: () => click(), expire: () => timeout()};
}

test('loads only on click with the verified legacy identity, then hides loading UI', () => {
    const app = fixture();
    assert.equal(app.scripts.length, 0);
    app.click();
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
    app.click();
    app.scripts[0].onerror();
    assert.equal(app.button.disabled, false);
    assert.match(app.status.textContent, /尚未載入/);
    app.click();
    assert.equal(app.scripts[0].removed, true);
    assert.equal(app.scripts.length, 2);
});

test('iframe timeout retries through Disqus reset without another embed script', () => {
    const app = fixture();
    app.click();
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
