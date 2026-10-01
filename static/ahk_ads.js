(function () {
    'use strict';
    const region = document.getElementById('ahk-ad');
    if (!region) return;
    const location = window.location;
    const preview = ['localhost', '127.0.0.1', '[::1]'].includes(location.hostname);
    const slot = region.dataset.adSlot;
    if (!['http:', 'https:'].includes(location.protocol) || location.pathname !== '/ahkblockly') return;
    if (!preview && (location.hostname !== 'papple23g-ahkcompiler.herokuapp.com' ||
        location.protocol !== 'https:' || !/^\d+$/.test(slot))) return;

    function initialize() {
        const column = document.getElementById('ahk_help_column');
        const frame = column && column.querySelector('iframe');
        if (!frame) return;
        readyObserver.disconnect();
        column.insertBefore(region, column.firstChild);
        let ad;
        let scriptReady = false;
        let pushed = false;
        let failed = false;
        let timeout;
        let statusObserver;
        function hide() {
            failed = true;
            region.hidden = true;
            clearTimeout(timeout);
            statusObserver.disconnect();
            sizeObserver.disconnect();
        }

        function update() {
            if (failed) return;
            region.hidden = frame.getBoundingClientRect().width < 300;
            if (region.hidden) return;
            if (preview) {
                document.getElementById('ahk-ad-preview').hidden = false;
                return;
            }
            if (!ad) {
                ad = document.createElement('ins');
                ad.className = 'adsbygoogle';
                ad.style.cssText = 'display:inline-block;width:300px;height:250px';
                ad.dataset.adClient = 'ca-pub-3626951597834728';
                ad.dataset.adSlot = slot;
                region.appendChild(ad);
                statusObserver = new MutationObserver(function () {
                    const status = ad.getAttribute('data-ad-status');
                    if (status === 'unfilled') hide();
                    if (status === 'filled') {
                        clearTimeout(timeout);
                        statusObserver.disconnect();
                    }
                });
                statusObserver.observe(ad, {attributes: true, attributeFilter: ['data-ad-status']});
                // ponytail: stop after 20 seconds; no retry or automatic ad refresh in this trial.
                timeout = setTimeout(hide, 20000);
                const script = document.createElement('script');
                script.async = true;
                script.crossOrigin = 'anonymous';
                script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3626951597834728';
                script.onerror = hide;
                script.onload = function () {
                    scriptReady = true;
                    update();
                };
                document.head.appendChild(script);
            }
            if (scriptReady && !pushed) {
                pushed = true;
                try {
                    (window.adsbygoogle = window.adsbygoogle || []).push({});
                } catch (_) {
                    hide();
                }
            }
        }
        const sizeObserver = new ResizeObserver(update);
        sizeObserver.observe(frame);
        update();
    }

    // Brython builds the help column after the server-rendered page is loaded.
    const readyObserver = new MutationObserver(initialize);
    readyObserver.observe(document.getElementById('div_subMainPage'), {childList: true, subtree: true});
    initialize();
}());
