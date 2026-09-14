from pathlib import Path
import unittest


class RuntimeTests(unittest.TestCase):
    def test_heroku_uses_one_python_version_declaration(self) -> None:
        self.assertFalse(Path('runtime.txt').exists())
        self.assertEqual(Path('.python-version').read_text(encoding='utf-8').strip(), '3.12')
