from http import HTTPStatus
from io import BytesIO
from unittest.mock import call, mock_open, patch
from uuid import UUID

from django.test import RequestFactory, SimpleTestCase

from myapp import views


TOKEN = '12345678-1234-4234-8234-123456789abc'
TOOL_URL = 'https://papple23g-ahkcompiler.herokuapp.com/ahkblockly'
INVALID_TOKENS = (
    '',
    'not-a-uuid',
    '12345678-1234-1234-8234-123456789abc',
    '12345678-1234-3234-8234-123456789abc',
    f'../{TOKEN}',
    f'..\\{TOKEN}',
    f'../../ahkfile1_30/{TOKEN}',
)


class CompileTests(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_cp_preserves_utf8_source_and_uses_a_v4_64bit_output(self) -> None:
        for source in (
            '; 64-bit\r\nMsgBox, 中文測試\r\n\r\nSend, {Enter}\r\n',
            '; 64-bit\nMsgBox, 符號：😀「引號」\n',
        ):
            with self.subTest(source=source):
                request = self.factory.post(
                    '/cp',
                    data=source.encode('utf-8'),
                    content_type='text/plain; charset=utf-8',
                )
                output = mock_open()
                with patch('myapp.views.uuid.uuid4', return_value=UUID(TOKEN)) as uuid4:
                    with patch('myapp.views.open', output, create=True):
                        with patch('myapp.views.os.system', return_value=0) as system:
                            with patch('builtins.print'):
                                response = views.cp(request)

                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertEqual(response.content.decode(), TOKEN)
                self.assertEqual(UUID(response.content.decode()).version, 4)
                uuid4.assert_called_once_with()
                output.assert_called_once_with(
                    f'ahkfile1_30/{TOKEN}.ahk', 'w', encoding='utf-8-sig',
                )
                output().write.assert_called_once_with('#SingleInstance force\n' + source)
                system.assert_called_once_with(
                    f'cd ahkfile1_30 & Ahk2Exe.exe /in {TOKEN}.ahk '
                    f'/out {TOKEN}.exe /bin "Unicode 64-bit.bin" /mpress 1',
                )

    def test_dl_streams_exe_and_accepts_the_legacy_foo_suffix(self) -> None:
        exe_bytes = b'MZ\x90\x00\x03\x00mock executable\xff'
        for token in (TOKEN, TOKEN + '?foo=cache-buster'):
            with self.subTest(token=token):
                executable = BytesIO(exe_bytes)
                request = self.factory.get('/dl', {'filename_key': token})
                with patch('myapp.views.open', return_value=executable, create=True) as opened:
                    response = views.dl(request)
                    try:
                        self.assertEqual(response.status_code, HTTPStatus.OK)
                        self.assertEqual(response['Content-Type'], 'application/octet-stream')
                        self.assertEqual(
                            response['Content-Disposition'], 'attachment;filename="myahk.exe"',
                        )
                        self.assertEqual(b''.join(response.streaming_content), exe_bytes)
                        opened.assert_called_once_with(f'ahkfile1_30/{TOKEN}.exe', 'rb')
                    finally:
                        response.close()
                self.assertTrue(executable.closed)

    def test_rm_removes_only_the_two_files_for_the_given_v4_token(self) -> None:
        request = self.factory.get('/rm', {'filename_key': TOKEN})
        paths = [f'ahkfile1_30/{TOKEN}.ahk', f'ahkfile1_30/{TOKEN}.exe']
        with patch('myapp.views.time.sleep') as sleep:
            with patch('myapp.views.os.path.isfile', return_value=True) as isfile:
                with patch('myapp.views.os.remove') as remove:
                    with patch('builtins.print'):
                        response = views.rm(request)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content.decode(), 'OKOK!' + TOKEN)
        sleep.assert_called_once_with(5)
        self.assertEqual(isfile.call_args_list, [call(path) for path in paths])
        self.assertEqual(remove.call_args_list, [call(path) for path in paths])

    def test_rm_skips_a_missing_source_and_removes_an_existing_exe(self) -> None:
        request = self.factory.get('/rm', {'filename_key': TOKEN})
        with patch('myapp.views.time.sleep'):
            with patch('myapp.views.os.path.isfile', side_effect=[False, True]):
                with patch('myapp.views.os.remove') as remove:
                    with patch('builtins.print'):
                        response = views.rm(request)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        remove.assert_called_once_with(f'ahkfile1_30/{TOKEN}.exe')

    def test_rm_can_repeat_when_both_files_are_already_missing(self) -> None:
        with patch('myapp.views.time.sleep') as sleep:
            with patch('myapp.views.os.path.isfile', return_value=False) as isfile:
                with patch('myapp.views.os.remove') as remove:
                    for _ in range(2):
                        response = views.rm(self.factory.get('/rm', {'filename_key': TOKEN}))
                        self.assertEqual(response.status_code, HTTPStatus.OK)
                        self.assertEqual(response.content.decode(), 'OKOK!' + TOKEN)

        self.assertEqual(sleep.call_args_list, [call(5), call(5)])
        self.assertEqual(isfile.call_args_list, [
            call(f'ahkfile1_30/{TOKEN}.ahk'), call(f'ahkfile1_30/{TOKEN}.exe'),
            call(f'ahkfile1_30/{TOKEN}.ahk'), call(f'ahkfile1_30/{TOKEN}.exe'),
        ])
        remove.assert_not_called()

    def test_invalid_tokens_never_open_or_remove_files_or_wait(self) -> None:
        with patch('myapp.views.open', create=True) as opened:
            with patch('myapp.views.time.sleep') as sleep:
                with patch('myapp.views.os.path.isfile') as isfile:
                    with patch('myapp.views.os.remove') as remove:
                        for token in INVALID_TOKENS:
                            for path, view in (('/dl', views.dl), ('/rm', views.rm)):
                                with self.subTest(path=path, token=token):
                                    response = view(self.factory.get(path, {'filename_key': token}))
                                    self.assertEqual(response.status_code, HTTPStatus.FOUND)
                                    self.assertEqual(response['Location'], TOOL_URL)

        opened.assert_not_called()
        sleep.assert_not_called()
        isfile.assert_not_called()
        remove.assert_not_called()

    def test_version_uuid_identifies_v4(self) -> None:
        self.assertEqual(views.version_uuid(TOKEN), 4)

    def test_version_uuid_distinguishes_other_uuid_versions(self) -> None:
        for version in (1, 3, 5):
            with self.subTest(version=version):
                token = str(UUID(TOKEN, version=version))
                self.assertEqual(views.version_uuid(token), version)

    def test_version_uuid_rejects_malformed_and_path_traversal_values(self) -> None:
        for token in INVALID_TOKENS:
            if token in (
                '12345678-1234-1234-8234-123456789abc',
                '12345678-1234-3234-8234-123456789abc',
            ):
                continue
            with self.subTest(token=token):
                self.assertIsNone(views.version_uuid(token))
