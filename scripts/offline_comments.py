import re

OFFLINE_COMMENTS = '<p id="comments"><a href="https://papple23g-ahkcompiler.herokuapp.com/ahkblockly#comments" target="_blank" rel="noopener noreferrer">前往網站閱讀與發表留言（需要連線）</a></p>'


def replace_online_comments(html: str) -> str:
    return re.sub(
        r'<!-- ONLINE-COMMENTS:START -->.*?<!-- ONLINE-COMMENTS:END -->',
        lambda _: OFFLINE_COMMENTS,
        html,
        flags=re.S,
    )
