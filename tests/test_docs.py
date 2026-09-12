from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('docs_tool', ROOT / 'scripts' / 'docs.py')
assert SPEC and SPEC.loader
DOCS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DOCS)


class DocsMigrationTests(unittest.TestCase):
    def test_validate_rejects_html_login_or_error_page(self) -> None:
        with self.assertRaises(ValueError):
            DOCS.validate_markdown('<!doctype html><html><body>login</body></html>')

    def test_rewrite_known_note_and_preserve_fragment(self) -> None:
        source = 'See https://hackmd.io/@papple12g/Hy0jtdnu3#section'
        self.assertEqual(DOCS.rewrite_urls(source, '/static/docs/', '.html'), 'See /static/docs/faq.html#section')

    def test_rewrite_unknown_note_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            DOCS.rewrite_urls('https://hackmd.io/not-a-known-note', '/static/docs/', '.html')

    def test_import_downloads_everything_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'templates').mkdir()
            (root / 'protable').mkdir()
            (root / 'static').mkdir()
            (root / 'templates' / 'sample.py').write_text(
                'url = "https://hackmd.io/@papple12g/Hy0jtdnu3"\n', encoding='utf-8'
            )
            ok = '# Note\n\n' + ('safe content ' * 10)
            calls = 0

            def fake_download(_: str) -> str:
                nonlocal calls
                calls += 1
                if calls == len(DOCS.SOURCES):
                    raise RuntimeError('last download failed')
                return ok

            with mock.patch.object(DOCS, 'download_note', side_effect=fake_download):
                with self.assertRaises(RuntimeError):
                    DOCS.migrate(root)
            self.assertFalse((root / 'docs').exists())
            self.assertIn('hackmd.io', (root / 'templates' / 'sample.py').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
