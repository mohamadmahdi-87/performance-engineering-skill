"""Mutation tests using isolated copies; no network or project-code execution."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'performance-engineering'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__', '.git'))

    def change(self, name, old, new):
        path = self.root / name
        text = path.read_text(encoding='utf-8')
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding='utf-8')

    def append(self, text):
        with (self.root / 'README.md').open('a', encoding='utf-8') as stream:
            stream.write('\n' + text + '\n')

    def fails(self, message):
        self.assertTrue(any(message in error for error in validator.validate(self.root)), message)

    def test_valid_package(self):
        self.assertEqual(validator.validate(self.root), [])

    def test_missing_file(self):
        (self.root / 'README.fa.md').unlink()
        self.fails('Missing required file')

    def test_missing_frontmatter(self):
        self.change('SKILL.md', '---', 'invalid')
        self.fails('frontmatter delimiters')

    def test_wrong_name(self):
        self.change('SKILL.md', 'name: performance-engineering', 'name: other')
        self.fails('frontmatter profile')

    def test_duplicate_metadata(self):
        self.change('SKILL.md', 'metadata:', 'name: duplicate\nmetadata:')
        self.fails('frontmatter profile')

    def test_long_description(self):
        self.change('SKILL.md', 'description: ', 'description: ' + 'x' * 1025)
        self.fails('1–1024')

    def test_entry_budget(self):
        with (self.root / 'SKILL.md').open('a', encoding='utf-8') as stream:
            stream.write('\n' * 201)
        self.fails('entry budget')

    def test_broken_link(self):
        self.append('[missing](absent.md)')
        self.fails('broken link')

    def test_escape(self):
        self.append('[outside](../outside.md)')
        self.fails('escapes package')

    def test_encoded_escape(self):
        self.append('[outside](%2e%2e/outside.md)')
        self.fails('escapes package')

    def test_bad_scheme(self):
        self.append('[bad](file:///etc/passwd)')
        self.fails('unsupported link')

    def test_external_links_not_fetched(self):
        self.append('[external](https://invalid.invalid/not-real)')
        self.assertEqual(validator.validate(self.root), [])

    def test_good_anchor(self):
        self.append('[section](SKILL.md#run-contract)')
        self.assertEqual(validator.validate(self.root), [])

    def test_bad_anchor(self):
        self.append('[section](SKILL.md#no-such-section)')
        self.fails('missing anchor')

    def test_unclosed_fence(self):
        self.append('```text\nexample')
        self.fails('unclosed fenced block')

    def test_fenced_link_ignored(self):
        self.append('~~~~text\n[example](missing.md)\n~~~\n~~~~')
        self.assertEqual(validator.validate(self.root), [])

    def test_duplicate_check(self):
        self.change('references/interface.md', '## P04 —', '## P01 —')
        self.fails('Duplicate check')
        self.fails('Check coverage mismatch')

    def test_extra_check(self):
        self.change('references/interface.md', '## P01 —', '## P49 —')
        self.fails('Check coverage mismatch')

    def test_missing_required_block(self):
        for field in ('Applies', 'Steps', 'Verify', 'Risks', 'Reverse'):
            with self.subTest(field=field):
                path = self.root / 'references/interface.md'
                original = path.read_text(encoding='utf-8')
                self.change('references/interface.md', f'**{field}:**', '**Other:**')
                self.fails(f'nonempty {field} block')
                path.write_text(original, encoding='utf-8')

    def test_router_duplicate(self):
        self.change('references/routing.md', '| P02 |', '| P01 |')
        self.fails('exactly once')

    def test_router_wrong_module(self):
        self.change('references/routing.md', '| Loading placeholders | interface |', '| Loading placeholders | assets |')
        self.fails('Router module mismatch')

    def test_invalid_utf8(self):
        (self.root / 'README.fa.md').write_bytes(b'\xff')
        self.fails('cannot read UTF-8')

    def test_missing_root(self):
        self.assertIn('Not a directory', validator.validate(self.root / 'absent')[0])

    def test_cli_exit_codes(self):
        command = [sys.executable, str(ROOT / 'scripts/validate.py'), '--root', str(self.root)]
        good = subprocess.run(command, capture_output=True, text=True, timeout=20)
        self.assertEqual(good.returncode, 0, good.stderr)
        (self.root / 'SKILL.md').unlink()
        bad = subprocess.run(command, capture_output=True, text=True, timeout=20)
        self.assertEqual(bad.returncode, 1, bad.stderr)
        self.assertIn('FAIL:', bad.stdout)

    def test_validator_is_read_only(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        validator.validate(self.root)
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
