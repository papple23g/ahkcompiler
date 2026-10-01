import re


def remove_online_ads(html: str) -> str:
    offline_html = re.sub(
        r'<!-- ONLINE-ADS:START -->.*?<!-- ONLINE-ADS:END -->',
        '',
        html,
        flags=re.S,
    )
    offline_html = re.sub(
        r'<script\b(?=[^>]*\ssrc\s*=\s*[\"\']'
        r'https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js'
        r'(?:\?[^\"\']*)?[\"\'])[^>]*>\s*</script\s*>',
        '',
        offline_html,
        flags=re.I,
    )
    if any(token in offline_html for token in (
        'ONLINE-ADS:', 'adsbygoogle', 'data-ad-client', 'data-ad-slot',
    )):
        raise ValueError('廣告標記不完整或仍有廣告程式，已停止離線匯出。')
    return offline_html
