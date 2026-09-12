/* Keep the verified legacy identity: Disqus thread 8080995238. */
(function () {
    'use strict';
    var button = document.getElementById('comments-load');
    var status = document.getElementById('comments-status');
    if (!button || !status || window.location.protocol === 'file:') return;

    var timer;
    var script;
    var loaded = false;
    function ready() {
        loaded = true;
        clearTimeout(timer);
        button.hidden = true;
        status.textContent = '';
    }
    function failed() {
        if (loaded) return;
        clearTimeout(timer);
        button.disabled = false;
        button.textContent = '重試載入留言';
        status.textContent = '留言尚未載入。請檢查網路或內容封鎖設定後重試，也可開啟下方原討論串。';
    }
    window.disqus_config = function () {
        this.page.url = 'https://hackmd.io/%40papple23g/r1RuM08tB';
        this.page.identifier = 'r1RuM08tB';
        this.callbacks.onReady = [ready];
    };
    button.addEventListener('click', function () {
        button.disabled = true;
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
    });
}());
