/* Keep the verified legacy identity: Disqus thread 8080995238. */
(function () {
    'use strict';
    var button = document.getElementById('comments-load');
    var status = document.getElementById('comments-status');
    var fallback = document.getElementById('comments-fallback');
    if (!button || !status || window.location.protocol === 'file:') return;

    var timer;
    var script;
    var loaded = false;
    function ready() {
        loaded = true;
        clearTimeout(timer);
        button.hidden = true;
        if (fallback) fallback.hidden = true;
        status.textContent = '';
    }
    function failed() {
        if (loaded) return;
        clearTimeout(timer);
        button.disabled = false;
        button.hidden = false;
        if (fallback) fallback.hidden = false;
        button.textContent = '重試載入留言';
        status.textContent = '留言尚未載入。請檢查網路或內容封鎖設定後重試，也可開啟下方原討論串。';
    }
    window.disqus_config = function () {
        this.page.url = 'https://hackmd.io/%40papple23g/r1RuM08tB';
        this.page.identifier = 'r1RuM08tB';
        this.callbacks.onReady = [ready];
    };
    function load() {
        loaded = false;
        clearTimeout(timer);
        button.disabled = true;
        button.hidden = true;
        if (fallback) fallback.hidden = true;
        status.textContent = '正在載入留言…';
        timer = setTimeout(failed, 20000);
        try {
            if (window.DISQUS && typeof window.DISQUS.reset === 'function') {
                window.DISQUS.reset({reload: true, config: window.disqus_config});
            } else {
                if (script) script.remove();
                script = document.createElement('script');
                script.src = 'https://ahkcompiler.disqus.com/embed.js';
                script.async = true;
                script.onerror = failed;
                document.head.appendChild(script);
            }
        } catch (error) {
            failed();
        }
    }
    button.addEventListener('click', load);
    var scheduled = false;
    function schedule() {
        if (scheduled) return;
        scheduled = true;
        // Let body.onload start Brython before adding third-party resources.
        setTimeout(load, 0);
    }
    if (document.readyState === 'complete') {
        schedule();
    } else {
        window.addEventListener('load', schedule, {once: true});
    }
}());
