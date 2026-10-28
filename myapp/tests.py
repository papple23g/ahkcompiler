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


import subprocess
import tempfile
import uuid
from pathlib import Path
from unittest import mock


class CompileEndpointTests(SimpleTestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        patcher = mock.patch('myapp.views.COMPILER_DIR', self.dir)
        patcher.start()
        self.addCleanup(patcher.stop)

    def post(self, body: str = '64-bit\nMsgBox hi'):
        return self.client.post('/cp', data=body, content_type='text/plain')

    def fake_run(self, write_exe: bool = True, content: bytes = b'MZ'):
        def run(args, **kwargs):
            if write_exe:
                (self.dir / args[args.index('/out') + 1]).write_bytes(content)
            return subprocess.CompletedProcess(args, 0)
        return run

    def assert_clean(self) -> None:
        self.assertEqual(list(self.dir.iterdir()), [])

    def test_success_uses_absolute_compiler_without_shell(self) -> None:
        with mock.patch('myapp.views.subprocess.run', side_effect=self.fake_run()) as run:
            response = self.post()
        self.assertEqual(response.status_code, 200)
        key = response.content.decode()
        self.assertEqual(uuid.UUID(key).version, 4)
        self.assertTrue((self.dir / f'{key}.exe').is_file())
        argv, kwargs = run.call_args[0][0], run.call_args[1]
        self.assertTrue(Path(argv[0]).is_absolute())
        self.assertEqual(Path(argv[0]).name, 'Ahk2Exe.exe')
        self.assertIs(kwargs['shell'], False)
        self.assertEqual(kwargs['cwd'], self.dir)
        self.assertIn('timeout', kwargs)

    def test_nonzero_exit_returns_error_and_cleans_up(self) -> None:
        err = subprocess.CalledProcessError(1, 'Ahk2Exe.exe')
        with mock.patch('myapp.views.subprocess.run', side_effect=err):
            response = self.post()
        self.assertEqual(response.status_code, 500)
        self.assert_clean()

    def test_timeout_returns_error_and_cleans_up(self) -> None:
        err = subprocess.TimeoutExpired('Ahk2Exe.exe', 30)
        with mock.patch('myapp.views.subprocess.run', side_effect=err):
            response = self.post()
        self.assertEqual(response.status_code, 500)
        self.assert_clean()

    def test_missing_compiler_returns_error(self) -> None:
        with mock.patch('myapp.views.subprocess.run', side_effect=FileNotFoundError):
            response = self.post()
        self.assertEqual(response.status_code, 500)
        self.assert_clean()

    def test_missing_or_empty_output_returns_error(self) -> None:
        for fake in (self.fake_run(write_exe=False), self.fake_run(content=b'')):
            with self.subTest(fake=fake):
                with mock.patch('myapp.views.subprocess.run', side_effect=fake):
                    response = self.post()
                self.assertEqual(response.status_code, 500)
                self.assertEqual(response.content, b'compile failed')
                self.assert_clean()

    def test_malformed_input_fails_gracefully(self) -> None:
        with mock.patch('myapp.views.subprocess.run', side_effect=self.fake_run()):
            response = self.post('')
        self.assertIn(response.status_code, (200, 500))
        self.assertNotIn(b'Traceback', response.content)

    def test_dl_and_rm_reject_non_uuid_keys(self) -> None:
        for path in ('/dl', '/rm'):
            for key in ('../../etc/passwd', 'abc', '..%2f..%2fsecret'):
                with self.subTest(path=path, key=key):
                    response = self.client.get(path, {'filename_key': key})
                    self.assertEqual(response.status_code, 302)
