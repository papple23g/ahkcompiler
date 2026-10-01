from pathlib import Path
import runpy
from types import SimpleNamespace
import unittest
from unittest.mock import mock_open, patch

from scripts.offline_ads import remove_online_ads
from scripts.offline_comments import OFFLINE_COMMENTS


class OfflineAdsTests(unittest.TestCase):
    def test_export_removes_ads_and_keeps_comments_replacement(self) -> None:
        comments = Path('templates/disqus_comments.html').read_text(encoding='utf-8')
        page = '''<body><main>tool</main>
<!-- ONLINE-ADS:START -->
<ins class="adsbygoogle" data-ad-client="ca-pub-test" data-ad-slot="123"></ins>
<!-- ONLINE-ADS:END -->
<script type="text/python">
doc['div_subMainPage']<=div_iframe_elt
</script>
<!-- ONLINE-ADS:START -->
<script src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-test"></script>
<script>(window.adsbygoogle = window.adsbygoogle || []).push({});</script>
<!-- ONLINE-ADS:END -->
''' + comments + '</body>'
        output = mock_open()
        with patch('requests.get', return_value=SimpleNamespace(text=page)) as get:
            with patch('builtins.open', output):
                runpy.run_path('onlineToOffline.py', run_name='__main__')
        self.assertEqual(get.call_count, 2)
        self.assertEqual(output().write.call_count, 2)
        for call in output().write.call_args_list:
            result = call.args[0]
            self.assertIn('<main>tool</main>', result)
            self.assertIn("#doc['div_subMainPage']<=div_iframe_elt", result)
            self.assertIn(OFFLINE_COMMENTS, result)
            for removed in ('ONLINE-ADS:', 'adsbygoogle', 'data-ad-client',
                            'data-ad-slot', 'ca-pub-test', 'comments.js', 'disqus_thread'):
                self.assertNotIn(removed, result)

    def test_incomplete_or_unmarked_ads_stop_export(self) -> None:
        for page in (
            '<!-- ONLINE-ADS:START --><script>adSetup()</script>',
            '<!-- ONLINE-ADS:END -->',
            '<script src="adsbygoogle.js?client=ca-pub-test"></script>',
            '<script src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js">adSetup()</script>',
            '<ins data-ad-slot="123"></ins>',
            '<ins data-ad-client="ca-pub-test"></ins>',
        ):
            with self.subTest(page=page), self.assertRaises(ValueError):
                remove_online_ads(page)

    def test_export_removes_legacy_loader_and_preserves_other_scripts(self) -> None:
        other_scripts = '''<script src="/static/workspace.js"></script>
<script>window.toolReady = true;</script>'''
        page = '''<body><main>tool</main>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-test"
    crossorigin="anonymous">
</script>
''' + other_scripts + '</body>'
        output = mock_open()
        with patch('requests.get', return_value=SimpleNamespace(text=page)) as get:
            with patch('builtins.open', output):
                runpy.run_path('onlineToOffline.py', run_name='__main__')
        self.assertEqual(get.call_count, 2)
        self.assertEqual(output().write.call_count, 2)
        for call in output().write.call_args_list:
            result = call.args[0]
            self.assertIn('<main>tool</main>', result)
            self.assertIn('<script src="lib/workspace.js"></script>', result)
            self.assertIn('<script>window.toolReady = true;</script>', result)
            self.assertNotIn('adsbygoogle', result)
            self.assertNotIn('ca-pub-test', result)

    def test_page_without_ads_is_unchanged(self) -> None:
        page = '<meta name="google-adsense-account" content="ca-pub-test"><body>tool</body>'
        self.assertEqual(remove_online_ads(page), page)
