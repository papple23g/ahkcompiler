from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCES: dict[str, tuple[str, str]] = {
    'usage': ('AHK 語法產生器說明', 'https://hackmd.io/@papple12g/rJvq8d2uh'),
    'faq': ('常見問題', 'https://hackmd.io/@papple12g/Hy0jtdnu3'),
    'about': ('關於本站', 'https://hackmd.io/@papple12g/B12AuO2d3'),
    'changelog-ahktool': ('填表版更新日誌', 'https://hackmd.io/@papple12g/rk3yqOnO2'),
    'changelog-ahkblockly': ('積木版更新日誌', 'https://hackmd.io/@papple12g/SJ1fcu2On'),
    'security': ('執行檔與防毒風險說明', 'https://hackmd.io/1cw5qjUHR4avs__Vmw9YVg'),
    'legacy-note-hcal': ('舊版離線頁面內嵌文件', 'https://hackmd.io/hcAlG6oeQNO1jpILguR5hw'),
    'legacy-note-r1ru': ('舊版離線頁面內嵌文件 2', 'https://hackmd.io/@papple23g/r1RuM08tB'),
}
URL_RE = re.compile(r"https?://hackmd\.io/(?!_uploads/)[^\s\"'<>\)\]]+", re.IGNORECASE)
TEXT_EXTENSIONS = {'.py', '.html', '.js', '.css', '.md', '.json'}


class NoteSource(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tag: str | None = None
        self.parts: list[str] = []
        self.nested = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.tag is not None:
            self.nested = True
        elif tag in {'textarea', 'div'} and dict(attrs).get('id') == 'doc':
            self.tag = tag

    def handle_endtag(self, tag: str) -> None:
        if tag == self.tag:
            self.tag = None

    def handle_data(self, data: str) -> None:
        if self.tag is not None:
            self.parts.append(data)


def validate_markdown(text: str) -> str:
    text = text.lstrip('\ufeff').replace('\r\n', '\n')
    if len(text.strip()) < 30 or re.match(r'\s*(?:<!doctype|<html\b|<head\b)', text, re.I):
        raise ValueError('Response is empty, an error, or an HTML page, not note Markdown')
    if not re.search(r'(?m)^(?:#{1,6}\s|---\s*$|[-*>]\s|\d+\.\s)', text):
        raise ValueError('Response does not contain recognizable Markdown')
    return text


def download_note(url: str) -> str:
    note_id = urlsplit(url).path.rsplit('/', 1)[-1]
    candidates = [url + '/download', 'https://hackmd.io/' + note_id + '/download', url]
    errors: list[str] = []
    for candidate in candidates:
        try:
            request = Request(candidate, headers={'User-Agent': 'ahkcompiler-docs-migration/1.0'})
            with urlopen(request, timeout=25) as response:
                if urlsplit(response.url).hostname != 'hackmd.io':
                    raise ValueError('Unexpected redirect host')
                data = response.read(4 * 1024 * 1024 + 1)
            if len(data) > 4 * 1024 * 1024:
                raise ValueError('Note exceeds the 4 MiB safety limit')
            text = data.decode('utf-8-sig')
            if re.search(r'<!doctype|<html\b', text, re.I):
                parser = NoteSource()
                parser.feed(text)
                if parser.nested or not parser.parts:
                    raise ValueError('No unrendered note source found in HTML')
                text = ''.join(parser.parts)
            return validate_markdown(text)
        except (HTTPError, URLError, TimeoutError, UnicodeError, ValueError) as error:
            errors.append(f'{candidate}: {error}')
    raise RuntimeError('Could not export note; no files were replaced:\n' + '\n'.join(errors))


def rewrite_urls(text: str, prefix: str, suffix: str) -> str:
    aliases: dict[str, str] = {}
    for slug, (_, url) in SOURCES.items():
        path = urlsplit(url).path.rstrip('/')
        aliases[path] = slug
        aliases[path.rsplit('/', 1)[-1]] = slug

    def replace(match: re.Match[str]) -> str:
        parsed = urlsplit(match.group(0))
        path = unquote(parsed.path).rstrip('/')
        slug = aliases.get(path) or aliases.get(path.rsplit('/', 1)[-1])
        if slug is None:
            raise ValueError('Unmapped HackMD URL: ' + match.group(0))
        fragment = '#' + parsed.fragment if parsed.fragment else ''
        return prefix + slug + suffix + fragment

    return URL_RE.sub(replace, text)


def migrate(root: Path = ROOT) -> None:
    content_dir = root / 'docs' / 'content'
    if any((content_dir / f'{slug}.md').exists() for slug in SOURCES):
        raise RuntimeError('Local documents already exist; refusing to overwrite local edits')
    originals = {slug: download_note(url) for slug, (_, url) in SOURCES.items()}
    documents = {slug: rewrite_urls(text, '', '.md') for slug, text in originals.items()}
    replacements: dict[Path, str] = {}
    for dirname in ('templates', 'protable', 'static'):
        base = root / dirname
        if not base.exists():
            continue
        for path in sorted(base.rglob('*')):
            if not path.is_file() or path.suffix not in TEXT_EXTENSIONS:
                continue
            text = path.read_text(encoding='utf-8')
            if URL_RE.search(text):
                prefix = 'docs/' if dirname == 'protable' else '/static/docs/'
                replacements[path] = rewrite_urls(text, prefix, '.html')
    offline = root / 'onlineToOffline.py'
    if offline.exists():
        text = offline.read_text(encoding='utf-8')
        if 'import shutil' not in text:
            text = text.replace('import os\n', 'import os\nimport shutil\n', 1)
        marker = '    need_to_replace_str_pairList_list=[\n'
        if marker not in text:
            raise ValueError('Offline exporter changed; review documentation paths manually')
        text = text.replace(marker, marker + "        ['/static/docs/', 'docs/'],\n", 1)
        text += '\n# Include pre-rendered local documentation in future offline exports.\n'
        text += "shutil.copytree(os.path.join(dir_path, 'static', 'docs'), os.path.join(dir_path, 'protable', 'docs'), dirs_exist_ok=True)\n"
        replacements[offline] = text
    content_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, dict[str, str | int]] = {}
    for slug, text in documents.items():
        (content_dir / f'{slug}.md').write_text(text, encoding='utf-8')
        report[slug] = {
            'source': SOURCES[slug][1],
            'source_sha256': hashlib.sha256(originals[slug].encode()).hexdigest(),
            'source_bytes': len(originals[slug].encode()),
            'local_sha256': hashlib.sha256(text.encode()).hexdigest(),
        }
    for path, text in replacements.items():
        path.write_text(text, encoding='utf-8')
    (root / 'docs' / 'migration-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def prepare_markdown(text: str) -> str:
    text = re.sub(r'\A---\s*\n.*?\n---\s*(?:\n|$)', '', text, count=1, flags=re.S)
    text = re.sub(r'<style\b[^>]*>.*?</style>', '', text, flags=re.I | re.S)
    slugs = '|'.join(re.escape(slug) for slug in SOURCES)
    text = re.sub(rf'\b({slugs})\.md(?=[#\)\"\s>])', r'\1.html', text)
    return text


def render(text: str, title: str, slug: str) -> str:
    import markdown
    import nh3
    rendered = markdown.markdown(prepare_markdown(text), extensions=['extra', 'toc', 'sane_lists'])
    attributes = {tag: set(values) for tag, values in nh3.ALLOWED_ATTRIBUTES.items()}
    attributes['*'] = {'id', 'title'}
    body = nh3.clean(rendered, attributes=attributes, clean_content_tags={'script', 'style', 'iframe'}, url_schemes={'http', 'https', 'mailto'})
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' https: data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"><title>{html.escape(title)}</title><style>body{{max-width:960px;margin:0 auto;padding:20px;font:16px/1.7 system-ui,sans-serif;overflow-wrap:anywhere;color:#24292f;background:white}}img{{max-width:100%;height:auto}}pre{{overflow:auto;padding:12px;background:#f6f8fa}}code{{font-family:Consolas,monospace}}table{{border-collapse:collapse;display:block;overflow:auto}}th,td{{padding:6px 12px;border:1px solid #d0d7de}}blockquote{{margin-left:0;padding-left:16px;border-left:4px solid #d0d7de}}a{{color:#0969da}}footer{{margin-top:32px;border-top:1px solid #d0d7de;padding-top:12px;font-size:14px}}</style></head><body><main>{body}</main><footer>文件由儲存庫內的 Markdown 產生。 <a href="{slug}.md">Markdown 原文</a></footer></body></html>\n'''


def build(root: Path = ROOT, check: bool = False) -> None:
    expected: dict[Path, str] = {}
    for slug, (title, _) in SOURCES.items():
        source = root / 'docs' / 'content' / f'{slug}.md'
        text = validate_markdown(source.read_text(encoding='utf-8'))
        if URL_RE.search(text):
            raise ValueError('Unmigrated HackMD link in ' + str(source))
        page = render(text, title, slug)
        for folder in (root / 'static' / 'docs', root / 'protable' / 'docs'):
            expected[folder / f'{slug}.html'] = page
            expected[folder / f'{slug}.md'] = text
    for path, text in expected.items():
        if check:
            if not path.exists() or path.read_text(encoding='utf-8') != text:
                raise ValueError('Stale/missing generated document: ' + str(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
    for dirname in ('templates', 'protable', 'static'):
        for path in (root / dirname).rglob('*'):
            if path.is_file() and path.suffix in TEXT_EXTENSIONS and URL_RE.search(path.read_text(encoding='utf-8')):
                raise ValueError('Runtime HackMD reference remains: ' + str(path))


def main() -> None:
    parser = argparse.ArgumentParser(description='Import once, then build documentation entirely offline.')
    parser.add_argument('--import-hackmd', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.import_hackmd and args.check:
        parser.error('--import-hackmd and --check cannot be combined')
    if args.import_hackmd:
        migrate()
    build(check=args.check)


if __name__ == '__main__':
    main()
