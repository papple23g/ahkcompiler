from django.test import SimpleTestCase


HOSTS = ('127.0.0.1', 'papple23g-ahkcompiler.herokuapp.com')
DOCUMENT_SOURCES = {
    'ahktool': ('https://hackmd.io/@papple12g/rJvq8d2uh',),
    'ahkblockly': ('https://hackmd.io/@papple12g/rJvq8d2uh',),
    'about': ('https://hackmd.io/@papple12g/B12AuO2d3',),
    'faq': ('https://hackmd.io/@papple12g/Hy0jtdnu3',),
    'updateDiary': (
        'https://hackmd.io/@papple12g/rk3yqOnO2',
        'https://hackmd.io/@papple12g/SJ1fcu2On',
    ),
}


class SiteParityTests(SimpleTestCase):
    def test_every_page_preserves_production_document_sources(self) -> None:
        for host in HOSTS:
            for page, sources in DOCUMENT_SOURCES.items():
                with self.subTest(host=host, page=page):
                    response = self.client.get('/' + page, HTTP_HOST=host)
                    self.assertEqual(response.status_code, 200)
                    for source in sources:
                        self.assertContains(response, f'src="{source}"', count=1)
                    self.assertNotContains(response, '/static/docs/')
                    self.assertNotContains(response, 'ahkcompiler.papple23g.com')
                    self.assertNotContains(response, 'domain-migration-notice')

    def test_local_and_production_hosts_render_identically(self) -> None:
        for page in DOCUMENT_SOURCES:
            with self.subTest(page=page):
                local = self.client.get('/' + page, HTTP_HOST=HOSTS[0])
                production = self.client.get('/' + page, HTTP_HOST=HOSTS[1])
                self.assertEqual(local.content, production.content)

    def test_security_explanation_keeps_original_source(self) -> None:
        response = self.client.get('/ahkblockly')
        self.assertContains(response, 'https://hackmd.io/1cw5qjUHR4avs__Vmw9YVg?view')


class CommentsTests(SimpleTestCase):
    def test_blockly_hosts_have_one_widget_outside_the_document(self) -> None:
        for host in HOSTS:
            with self.subTest(host=host):
                response = self.client.get('/ahkblockly', HTTP_HOST=host)
                self.assertContains(response, 'id="disqus_thread"', count=1)
                self.assertContains(response, '/static/comments.js', count=1)
                self.assertEqual(response['Cross-Origin-Opener-Policy'], 'same-origin-allow-popups')

    def test_other_pages_do_not_load_comments(self) -> None:
        for page in ('ahktool', 'faq', 'about', 'updateDiary'):
            with self.subTest(page=page):
                response = self.client.get('/' + page)
                self.assertNotContains(response, 'disqus_thread')
                self.assertNotContains(response, 'comments.js')
                self.assertEqual(response['Cross-Origin-Opener-Policy'], 'same-origin')
