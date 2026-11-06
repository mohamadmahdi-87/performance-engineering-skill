"""Mutation tests using isolated copies; no network or project-code execution."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
REAL_SCANDIR = os.scandir
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'performance-engineering'
        shutil.copytree(
            ROOT,
            self.root,
            ignore=shutil.ignore_patterns(
                '.git', '__pycache__', '.pytest_cache', '.mypy_cache',
                '.ruff_cache', '.cache', '.tox', '.nox', '.venv', 'venv',
                'node_modules', '*.pyc',
            ),
        )

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

    def make_symlink(self, target, link, target_is_directory=False):
        try:
            os.symlink(target, link, target_is_directory=target_is_directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f'symlink creation unavailable: {type(exc).__name__}')
        def remove_link():
            if not os.path.lexists(link):
                return
            if target_is_directory and os.name == 'nt':
                os.rmdir(link)
            else:
                link.unlink()

        self.addCleanup(remove_link)

    def assert_no_external_enumeration(self, outside):
        outside = outside.resolve()
        enumerated = []

        def observe(path):
            candidate = Path(path).resolve()
            enumerated.append(candidate)
            return REAL_SCANDIR(path)

        with mock.patch.object(validator.os, 'scandir', side_effect=observe):
            errors = validator.validate(self.root)
        self.assertTrue(any('symlink or reparse point' in error for error in errors), errors)
        self.assertFalse(
            any(path == outside or outside in path.parents for path in enumerated),
            f'validator enumerated external target: {enumerated}',
        )

    def test_valid_package(self):
        self.assertEqual(validator.validate(self.root), [])

    def test_missing_file(self):
        (self.root / 'README.fa.md').unlink()
        self.fails('Missing required file')

    def test_validation_document_is_required(self):
        (self.root / 'docs/VALIDATION.md').unlink()
        self.fails('Missing required file: docs/VALIDATION.md')

    def test_missing_frontmatter(self):
        self.change('SKILL.md', '---', 'invalid')
        self.fails('frontmatter delimiters')

    def test_wrong_name(self):
        self.change('SKILL.md', 'name: performance-engineering', 'name: other')
        self.fails('name and package directory')

    def test_renamed_package_directory(self):
        renamed = self.root.with_name('renamed-skill')
        self.root.rename(renamed)
        self.root = renamed
        self.fails('name and package directory')

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

    def test_case_mismatch_in_file_and_directory(self):
        self.append('[wrong file case](sKILL.md)')
        self.append('[wrong directory case](References/routing.md)')
        errors = validator.validate(self.root)
        self.assertGreaterEqual(
            sum('link path has incorrect case' in error for error in errors), 2,
            errors,
        )

    def test_unicode_space_and_percent_encoded_link(self):
        filename = 'گزارش نمونه.md'
        target = self.root / 'assets' / filename
        target.write_text('# بخش ویژه\n', encoding='utf-8')
        encoded_path = quote(f'assets/{filename}', safe='/')
        encoded_anchor = quote('بخش-ویژه', safe='-')
        self.append(f'[encoded]({encoded_path}#{encoded_anchor})')
        self.assertEqual(validator.validate(self.root), [])

    def test_symlinked_directory_is_not_enumerated(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        (outside / 'secret.md').write_text('synthetic fixture', encoding='utf-8')
        self.make_symlink(outside, self.root / 'external-dir', target_is_directory=True)
        self.assert_no_external_enumeration(outside)

    def test_symlinked_file_is_not_read(self):
        outside = Path(self.temp.name) / 'outside.md'
        outside.write_text('synthetic fixture', encoding='utf-8')
        self.make_symlink(outside, self.root / 'assets' / 'external.md')
        outside_resolved = outside.resolve()
        reads = []
        original = Path.read_text

        def observe_read(path, *args, **kwargs):
            reads.append(Path(path).resolve())
            return original(path, *args, **kwargs)

        with mock.patch.object(Path, 'read_text', observe_read):
            errors = validator.validate(self.root)
        self.assertTrue(any('symlink or reparse point' in error for error in errors), errors)
        self.assertNotIn(outside_resolved, reads)

    @unittest.skipUnless(os.name == 'nt', 'Windows junctions are only available on Windows')
    def test_windows_junction_is_not_enumerated(self):
        shell = shutil.which('powershell.exe') or shutil.which('pwsh.exe')
        if not shell:
            self.skipTest('PowerShell is unavailable to create a temporary junction')
        outside = Path(self.temp.name) / 'junction-target'
        outside.mkdir()
        (outside / 'secret.md').write_text('synthetic fixture', encoding='utf-8')
        junction = self.root / 'external-junction'

        def quote_ps(value):
            return "'" + str(value).replace("'", "''") + "'"

        command = (
            'New-Item -ItemType Junction -Path '
            + quote_ps(junction)
            + ' -Target '
            + quote_ps(outside)
            + ' | Out-Null'
        )
        try:
            result = subprocess.run(
                [shell, '-NoLogo', '-NoProfile', '-NonInteractive', '-Command', command],
                capture_output=True, text=True, timeout=15,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            self.skipTest(f'temporary junction creation unavailable: {type(exc).__name__}')
        if result.returncode != 0 or not os.path.lexists(junction):
            self.skipTest('host could not create a temporary junction without changing privileges')
        self.addCleanup(lambda: os.rmdir(junction) if os.path.lexists(junction) else None)
        self.assert_no_external_enumeration(outside)

    def test_external_links_not_fetched(self):
        self.append('[external](https://invalid.invalid/not-real)')
        self.assertEqual(validator.validate(self.root), [])

    def test_good_anchor(self):
        self.append('[section](SKILL.md#run-contract)')
        self.append('[same file](#repository-identity)')
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

    def test_git_metadata_is_skipped_before_enumeration(self):
        git_dir = self.root / '.git'
        git_dir.mkdir()
        (git_dir / 'unrelated.md').write_text('synthetic metadata', encoding='utf-8')
        self.append('[metadata](.git/unrelated.md)')
        self.append('[case alias](.GIT/unrelated.md)')
        enumerated = []

        def observe(path):
            enumerated.append(Path(path))
            return REAL_SCANDIR(path)

        with mock.patch.object(validator.os, 'scandir', side_effect=observe):
            errors = validator.validate(self.root)
        self.assertTrue(any('unsupported or unreadable local link' in error for error in errors), errors)
        self.assertNotIn(git_dir, enumerated)

    def test_filesystem_listing_error_is_reported(self):
        def fail_examples(path):
            if Path(path) == self.root / 'examples':
                raise PermissionError('synthetic denied')
            return REAL_SCANDIR(path)

        with mock.patch.object(validator.os, 'scandir', side_effect=fail_examples):
            errors = validator.validate(self.root)
        self.assertTrue(
            any('cannot list directory (PermissionError)' in error for error in errors),
            errors,
        )

    def test_missing_root(self):
        self.assertIn('Cannot inspect package root', validator.validate(self.root / 'absent')[0])

    def test_cli_exit_codes(self):
        command = [sys.executable, str(ROOT / 'scripts/validate.py'), '--root', str(self.root)]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
        good = subprocess.run(command, capture_output=True, text=True, timeout=20, env=env)
        self.assertEqual(good.returncode, 0, good.stderr)
        (self.root / 'SKILL.md').unlink()
        bad = subprocess.run(command, capture_output=True, text=True, timeout=20, env=env)
        self.assertEqual(bad.returncode, 1, bad.stderr)
        self.assertIn('FAIL:', bad.stdout)

    def test_cli_root_from_different_working_directory(self):
        parent = Path(self.temp.name) / 'مسیر دارای فاصله'
        parent.mkdir()
        package = parent / 'performance-engineering'
        self.root.rename(package)
        self.root = package
        unrelated_cwd = Path(self.temp.name) / 'elsewhere'
        unrelated_cwd.mkdir()
        command = [sys.executable, str(ROOT / 'scripts/validate.py'), '--root', str(package)]
        result = subprocess.run(
            command, cwd=unrelated_cwd, capture_output=True, text=True, timeout=20,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1'),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validator_is_read_only(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        validator.validate(self.root)
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
