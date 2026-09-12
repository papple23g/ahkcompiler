from django.test import SimpleTestCase


class CommentsTests(SimpleTestCase):
    def test_blockly_hosts_have_one_widget_and_local_docs(self) -> None:
        for host in ('ahkcompiler.papple23g.com', 'papple23g-ahkcompiler.herokuapp.com'):
            with self.subTest(host=host):
                response = self.client.get('/ahkblockly', HTTP_HOST=host)
                self.assertContains(response, 'id="disqus_thread"', count=1)
                self.assertContains(response, '/static/comments.js', count=1)
                self.assertContains(response, '/static/docs/usage.html')
                self.assertEqual(response['Cross-Origin-Opener-Policy'], 'same-origin-allow-popups')

    def test_other_pages_do_not_load_comments(self) -> None:
        for page in ('ahktool', 'faq', 'about', 'updateDiary'):
            with self.subTest(page=page):
                response = self.client.get('/' + page)
                self.assertNotContains(response, 'disqus_thread')
                self.assertNotContains(response, 'comments.js')
                self.assertEqual(response['Cross-Origin-Opener-Policy'], 'same-origin')
