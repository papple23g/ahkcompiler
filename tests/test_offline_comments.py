from pathlib import Path
import unittest

from scripts.offline_comments import OFFLINE_COMMENTS, replace_online_comments


class OfflineCommentsTests(unittest.TestCase):
    def test_export_removes_entire_online_widget(self) -> None:
        widget = Path('templates/disqus_comments.html').read_text(encoding='utf-8')
        result = replace_online_comments('before' + widget + 'after')
        self.assertIn(OFFLINE_COMMENTS, result)
        self.assertNotIn('comments.js', result)
        self.assertNotIn('disqus_thread', result)
        self.assertNotIn('disqus.com', result)
        self.assertTrue(result.startswith('before'))
        self.assertTrue(result.endswith('after'))

    def test_unrelated_page_is_unchanged(self) -> None:
        self.assertEqual(replace_online_comments('<body>tool</body>'), '<body>tool</body>')

    def test_shipped_offline_page_has_only_link(self) -> None:
        page = Path('protable/ahkblockly.html').read_text(encoding='utf-8')
        self.assertIn(OFFLINE_COMMENTS, page)
        self.assertNotIn('comments.js', page)
        self.assertNotIn('disqus.com', page)
