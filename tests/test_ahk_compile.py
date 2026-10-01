import ast
from html import escape
from pathlib import Path
import re
from types import SimpleNamespace
from typing import Any
import unittest
from unittest.mock import AsyncMock, Mock
import warnings
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]


def load_functions(
    path: str,
    names: set[str],
    namespace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source = ROOT / path
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', SyntaxWarning)
        tree = ast.parse(source.read_text(encoding='utf-8'), filename=str(source))
    nodes = [node for node in tree.body if (
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names
    ) or (
        isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id in {
                'TAB_SPACE', 'FUNC_DICT', 'func_dict_key_set',
            } for target in node.targets
        )
    )]
    found = {node.name for node in nodes if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    if found != names:
        raise AssertionError(f'Missing production functions: {names - found}')
    if namespace is None:
        namespace = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), 'exec'), namespace)
    return namespace


# ponytail: XML selectors only; use browser checks for HTML parsing and actual DOM behaviour.
class XmlNode:
    def __init__(
        self,
        element: ElementTree.Element | None = None,
        parent: 'XmlNode | None' = None,
    ) -> None:
        self.element = element if element is not None else ElementTree.Element('div')
        self.parent = parent
        self.nodes = parent.nodes if parent is not None else {}
        self.nodes[id(self.element)] = self
        self.children = [XmlNode(child, self) for child in self.element]

    @property
    def attrs(self) -> dict[str, str]:
        return self.element.attrib

    @property
    def text(self) -> str:
        return ''.join(self.element.itertext())

    @property
    def innerHTML(self) -> str:
        return ''.join(ElementTree.tostring(child, encoding='unicode') for child in self.element)

    @innerHTML.setter
    def innerHTML(self, value: str) -> None:
        self.__init__(ElementTree.fromstring(f'<div>{value}</div>'))

    def select(self, selector: str) -> list['XmlNode']:
        xpath = re.sub(r'\[([a-z_]+)=', r'[@\1=', selector.replace('>', '/'))
        return [self.nodes[id(element)] for element in self.element.findall(f'.//{xpath}')]

    def select_one(self, selector: str) -> 'XmlNode | None':
        elements = self.select(selector)
        return elements[0] if elements else None

    def remove(self) -> None:
        if self.parent is not None:
            self.parent.element.remove(self.element)


def compile_xml(xml: str) -> str:
    namespace = load_functions('templates/ahkblockly.py', {
        'FindCurrent', 'XmlToAHK', 'ToFullWidthString', 'Comment',
        'AHK_value', 'AHK_statement', 'AHK_block',
    })
    output = SimpleNamespace(innerHTML='')
    namespace.update(DIV=XmlNode, doc={'textarea_ahk': output})
    namespace['XmlToAHK'](SimpleNamespace(
        type='input', currentTarget=SimpleNamespace(value=xml),
    ))
    return output.innerHTML


class AhkGenerationTests(unittest.TestCase):
    def test_default_hotkey_opens_the_expected_url(self) -> None:
        xml = '''<xml><block type="hotkey_execute"><value name="NAME">
          <block type="function_key"><field name="function_key">Ctrl</field>
            <value><block type="function_key"><field>Shift</field>
              <value><block type="normal_key"><field>A</field></block></value>
            </block></value>
          </block></value><statement name="DO"><block type="open">
            <value name="NAME"><block type="webpage">
              <field name="NAME">https://www.autohotkey.com/</field>
            </block></value>
          </block></statement></block></xml>'''
        self.assertEqual(compile_xml(xml), '^+A::Run % "https://www.autohotkey.com/"\n\n\n')

    def test_nested_arithmetic_and_variable_names(self) -> None:
        xml = '''<xml><block type="variables_set"><field name="VAR">等待 秒數</field>
          <value name="VALUE"><block type="math_arithmetic"><field name="OP">MULTIPLY</field>
            <value name="A"><block type="math_arithmetic"><field name="OP">ADD</field>
              <value name="A"><block type="math_number"><field name="NUM">2</field></block></value>
              <value name="B"><block type="math_number"><field name="NUM">3</field></block></value>
            </block></value>
            <value name="B"><block type="math_number"><field name="NUM">1000</field></block></value>
          </block></value></block></xml>'''
        self.assertEqual(compile_xml(xml), '等待_秒數 := ((2+3)*1000)\n\n')

    def test_text_comments_and_next_blocks_are_preserved(self) -> None:
        xml = '''<xml><block type="msgbox"><comment>第一行\n第二行</comment>
          <value><block type="text"><field>繁體中文 &amp; "引號" `</field></block></value>
          <next><block type="sleep"><value><block type="math_number">
            <field name="NUM"> 500 </field>
          </block></value></block></next>
        </block></xml>'''
        self.assertEqual(
            compile_xml(xml),
            ';第一行\n;第二行\nMsgbox % "繁體中文 & ""引號"" ``"\nSleep % 500\n\n',
        )

    def test_loop_indents_actions_and_reuses_its_counter(self) -> None:
        xml = '''<xml><block type="controls_repeat_ext">
          <value name="TIMES"><block type="math_number"><field name="NUM">3</field></block></value>
          <statement name="DO"><block type="sleep"><value><block type="math_number">
            <field name="NUM">10</field>
          </block></value></block></statement>
        </block></xml>'''
        self.assertRegex(
            compile_xml(xml),
            r'^loop_time_int_(\d+):=3\nLoop %loop_time_int_\1% \{\n    Sleep % 10\n\}\n\n$',
        )

    def test_shared_preamble_is_emitted_once_without_leaking_to_the_next_script(self) -> None:
        hotkey = '''<block type="hotkey_execute_with_setting">
          <value name="NAME"><block type="normal_key"><field>A</field></block></value>
          <statement name="SETTING"><block type="hotkey_execute_setting_ifwinactive">
            <field name="text">記事本</field>
          </block></statement>
          <statement name="DO"><block type="reload"/></statement>
        </block>'''
        namespace = load_functions('templates/ahkblockly.py', {
            'FindCurrent', 'XmlToAHK', 'ToFullWidthString', 'Comment',
            'AHK_value', 'AHK_statement', 'AHK_block',
        })
        output = SimpleNamespace(innerHTML='')
        namespace.update(DIV=XmlNode, doc={'textarea_ahk': output})
        for xml in (f'<xml>{hotkey}{hotkey}</xml>', '<xml/>'):
            namespace['XmlToAHK'](SimpleNamespace(
                type='input', currentTarget=SimpleNamespace(value=xml),
            ))
            if xml == '<xml/>':
                self.assertEqual(output.innerHTML, '')
            else:
                self.assertEqual(output.innerHTML.count('SetTitleMatchMode, 2\n'), 1)
                self.assertEqual(output.innerHTML.count('#IfWinActive, 記事本\nA::Reload\n#If\n'), 2)

    def test_empty_disabled_and_unconnected_value_blocks_do_not_emit_code(self) -> None:
        for xml in ('<xml/>', '''<xml>
          <block type="msgbox" disabled="true"><value><block type="text">
            <field>不應執行</field></block></value></block>
          <block type="text"><field>落單文字</field></block>
        </xml>'''):
            with self.subTest(xml=xml):
                self.assertEqual(compile_xml(xml).strip(), '')


class AhkExeDownloadTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.code = 'MsgBox % "繁體中文 <測試> & 引號"\r\nExitApp\r\n'
        self.encoded_code = escape(self.code)
        self.button = SimpleNamespace(text='下載.exe檔(64-bit)', disabled=False, classList=Mock())
        self.document = Mock()
        self.document.__getitem__ = Mock(return_value=SimpleNamespace(innerHTML=self.encoded_code))
        self.parser = Mock()
        self.parser.parseFromString.return_value = SimpleNamespace(body=SimpleNamespace(textContent=self.code))
        self.window = SimpleNamespace(
            DOMParser=SimpleNamespace(new=Mock(return_value=self.parser)),
            Uint8Array=SimpleNamespace(new=Mock(return_value=object())),
            Blob=SimpleNamespace(new=Mock(return_value=object())),
            URL=SimpleNamespace(
                createObjectURL=Mock(return_value='blob:unit-test'), revokeObjectURL=Mock(),
            ),
        )
        self.response = SimpleNamespace(status=200, data=SimpleNamespace(source=b'MZ-unit-test'))
        self.aio = SimpleNamespace(ajax=AsyncMock(return_value=self.response), sleep=AsyncMock())
        self.namespace = load_functions('templates/ahkblockly.py', {'DownloadAhkExe'})
        load_functions('templates/base_function.py', {'JavascriptSymbolDecoder'}, self.namespace)
        self.namespace.update(doc=self.document, window=self.window, aio=self.aio)

    async def download(self) -> None:
        await self.namespace['DownloadAhkExe'](SimpleNamespace(currentTarget=self.button))

    def assert_button_restored(self) -> None:
        self.assertFalse(self.button.disabled)
        self.assertEqual(self.button.text, '下載.exe檔(64-bit)')
        self.button.classList.add.assert_called_once_with('disabled_button')
        self.button.classList.remove.assert_called_once_with('disabled_button')
        self.aio.sleep.assert_awaited_once_with(3)

    async def test_success_posts_decoded_source_and_downloads_binary(self) -> None:
        async def compile_request(*args: Any, **kwargs: Any) -> SimpleNamespace:
            self.assertTrue(self.button.disabled)
            self.assertEqual(self.button.text, '轉譯中...')
            return self.response

        self.aio.ajax.side_effect = compile_request
        await self.download()
        self.aio.ajax.assert_awaited_once_with(
            'POST', 'https://papple23g-rest-ahk.zeabur.app/compile',
            data=self.code, headers={'Content-Type': 'text/plain'}, format='binary',
        )
        self.parser.parseFromString.assert_called_once_with(
            '<!doctype html><body>' + self.encoded_code, 'text/html',
        )
        self.window.Uint8Array.new.assert_called_once_with(self.response.data.source)
        self.window.Blob.new.assert_called_once_with(
            [self.window.Uint8Array.new.return_value], {'type': 'application/x-msdownload'},
        )
        link = self.document.createElement.return_value
        self.document.createElement.assert_called_once_with('a')
        self.assertEqual(link.href, 'blob:unit-test')
        self.assertEqual(link.download, 'myahk.exe')
        self.document.body.appendChild.assert_called_once_with(link)
        link.click.assert_called_once_with()
        self.document.body.removeChild.assert_called_once_with(link)
        self.window.URL.revokeObjectURL.assert_called_once_with('blob:unit-test')
        self.assert_button_restored()

    async def test_server_error_does_not_download_and_restores_the_button(self) -> None:
        self.response.status = 503
        await self.download()
        self.aio.ajax.assert_awaited_once()
        self.document.createElement.assert_not_called()
        self.window.Blob.new.assert_not_called()
        self.window.URL.createObjectURL.assert_not_called()
        self.assert_button_restored()

    async def test_network_exception_restores_the_button(self) -> None:
        self.aio.ajax.side_effect = ConnectionError('offline')
        with self.assertRaises(ConnectionError):
            await self.download()
        self.document.createElement.assert_not_called()
        self.assert_button_restored()
