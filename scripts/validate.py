#!/usr/bin/env python3
"""Offline, read-only checks for this package; not a general Markdown/YAML parser."""
from __future__ import annotations

import argparse
from collections import Counter
import os
from pathlib import Path
from pathlib import PurePosixPath
import re
import stat
from urllib.parse import unquote, urlsplit

SKILL_NAME = 'performance-engineering'
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
MODULES = ('interface', 'assets', 'data', 'services', 'runtime',
           'observability', 'safety-delivery', 'ai-compute')
IDS = {f'P{i:02}' for i in range(1, 49)}
REQUIRED = (
    'SKILL.md', 'README.md', 'README.fa.md', 'CONTRIBUTING.md', 'CHANGELOG.md',
    'docs/PUBLISHING.md', 'docs/PROVENANCE.md', 'docs/VALIDATION.md',
    'examples/scenarios.md',
    'assets/report-template.md', 'assets/experiment-template.md',
    'scripts/validate.py', 'tests/test_validate.py', '.github/workflows/validate.yml',
    *(f'references/{name}.md' for name in (*MODULES, 'routing', 'measurement',
                                          'workflow', 'interactions', 'recovery')),
)


def unfenced(text: str, label: str, errors: list[str]) -> str:
    """Exclude fenced examples from link/heading checks; detect unclosed fences."""
    marker = ''
    result = []
    for line in text.splitlines():
        match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if not marker and match:
            marker = match[1]
        elif marker and match and match[1][0] == marker[0] and len(match[1]) >= len(marker) and not match[2].strip():
            marker = ''
        elif not marker:
            result.append(line)
    if marker:
        errors.append(f'{label}: unclosed fenced block')
    return '\n'.join(result)


def anchors(text: str) -> set[str]:
    """GitHub-style anchors for the simple ATX headings used in this package."""
    result: set[str] = set()
    counts: Counter[str] = Counter()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        base = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        suffix = f'-{counts[base]}' if counts[base] else ''
        result.add(base + suffix)
        counts[base] += 1
    return result


def is_reparse_point(info: os.stat_result) -> bool:
    """Detect links and Windows junctions without following them (Python 3.10+)."""
    attributes = getattr(info, 'st_file_attributes', 0)
    return stat.S_ISLNK(info.st_mode) or bool(attributes & FILE_ATTRIBUTE_REPARSE_POINT)


def read_markdown(root: Path, errors: list[str]) -> tuple[dict[str, str], dict[str, str]]:
    """Walk top-down without following symlinks, junctions, or other reparse points."""
    raw: dict[str, str] = {}
    texts: dict[str, str] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        directory_rel = directory.relative_to(root).as_posix()
        label = directory_rel or '.'
        try:
            info = os.lstat(directory)
        except OSError as exc:
            errors.append(f'{label}: cannot inspect directory ({type(exc).__name__})')
            continue
        if is_reparse_point(info):
            errors.append(f'{label}: symlink or reparse point is not supported')
            continue
        if not stat.S_ISDIR(info.st_mode):
            errors.append(f'{label}: expected a directory')
            continue
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    # Git metadata is outside the package validation scope. Skip it
                    # before statting or opening the directory.
                    if entry.name.casefold() == '.git':
                        continue
                    path = Path(entry.path)
                    rel = (PurePosixPath(directory_rel) / entry.name).as_posix()
                    try:
                        entry_info = entry.stat(follow_symlinks=False)
                    except OSError as exc:
                        errors.append(f'{rel}: cannot inspect entry ({type(exc).__name__})')
                        continue
                    if is_reparse_point(entry_info):
                        errors.append(f'{rel}: symlink or reparse point is not supported')
                        continue
                    if stat.S_ISDIR(entry_info.st_mode):
                        pending.append(path)
                        continue
                    if not stat.S_ISREG(entry_info.st_mode) or path.suffix != '.md':
                        continue
                    try:
                        text = path.read_text(encoding='utf-8')
                    except (UnicodeError, OSError) as exc:
                        errors.append(f'{rel}: cannot read UTF-8 ({type(exc).__name__})')
                        continue
                    raw[rel] = text
                    texts[rel] = unfenced(text, rel, errors)
        except OSError as exc:
            errors.append(f'{label}: cannot list directory ({type(exc).__name__})')
    return raw, texts


def resolve_local_path(
    root: Path, source: PurePosixPath, raw_path: str
) -> tuple[PurePosixPath | None, os.stat_result | None, str | None]:
    """Resolve a package-local path component by component, requiring exact case."""
    try:
        decoded = unquote(raw_path)
    except (UnicodeError, ValueError):
        return None, None, 'unsupported'
    if not decoded:
        parts = list(source.parts)
    else:
        if decoded.startswith('/') or '\\' in decoded or '\x00' in decoded:
            return None, None, 'unsupported'
        components = decoded.split('/')
        if any(':' in component for component in components):
            return None, None, 'unsupported'
        parts = [] if source.as_posix() == '.' else list(source.parent.parts)
        for index, component in enumerate(components):
            if component in ('', '.'):
                continue
            if component.casefold() == '.git':
                return None, None, 'unsupported'
            if component == '..':
                if not parts:
                    return None, None, 'escape'
                parts.pop()
                continue

            directory = root.joinpath(*parts)
            try:
                directory_info = os.lstat(directory)
                if is_reparse_point(directory_info):
                    return None, None, 'reparse'
                if not stat.S_ISDIR(directory_info.st_mode):
                    return None, None, 'not-directory'
                exact = None
                case_mismatch = False
                with os.scandir(directory) as entries:
                    for entry in entries:
                        if entry.name == component:
                            exact = entry
                            break
                        if entry.name.casefold() == component.casefold():
                            case_mismatch = True
            except OSError:
                return None, None, 'unreadable'

            if exact is None:
                return None, None, 'case' if case_mismatch else 'missing'
            try:
                exact_info = exact.stat(follow_symlinks=False)
            except OSError:
                return None, None, 'unreadable'
            if is_reparse_point(exact_info):
                return None, None, 'reparse'
            has_more = any(part != '' for part in components[index + 1:])
            if has_more and not stat.S_ISDIR(exact_info.st_mode):
                return None, None, 'not-directory'
            parts.append(exact.name)

    relative = PurePosixPath(*parts) if parts else PurePosixPath('.')
    target = root if relative.as_posix() == '.' else root.joinpath(*relative.parts)
    try:
        info = os.lstat(target)
    except OSError:
        return None, None, 'missing'
    if is_reparse_point(info):
        return None, None, 'reparse'
    return relative, info, None


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        root = Path(os.path.abspath(os.fspath(root)))
        root_info = os.lstat(root)
    except (OSError, TypeError, ValueError) as exc:
        return [f'Cannot inspect package root ({type(exc).__name__})']
    if is_reparse_point(root_info):
        return ['Package root must not be a symlink or reparse point']
    if not stat.S_ISDIR(root_info.st_mode):
        return ['Package root is not a directory']

    raw, texts = read_markdown(root, errors)
    for name in REQUIRED:
        relative, info, reason = resolve_local_path(root, PurePosixPath('.'), name)
        if reason == 'missing':
            errors.append(f'Missing required file: {name}')
        elif reason == 'case':
            errors.append(f'Required file path has incorrect case: {name}')
        elif reason:
            errors.append(f'Required file path cannot be used ({reason}): {name}')
        elif info is None or not stat.S_ISREG(info.st_mode):
            errors.append(f'Required path is not a regular file: {name}')

    skill = raw.get('SKILL.md')
    if skill is not None:
        front = re.match(r'\A---\n(.*?)\n---(?:\n|$)', skill, re.S)
        if not front:
            errors.append('SKILL.md: missing YAML frontmatter delimiters')
        else:
            # Deliberately narrow: plain single-line name/description, then metadata.
            pattern = (r'name: ([a-z0-9]+(?:-[a-z0-9]+)*)\n'
                       r'description: ([^\n]+)\nmetadata:\n'
                       r'  author: ([^\n]+)\n  version: "(\d+\.\d+\.\d+)"')
            profile = re.fullmatch(pattern, front[1])
            if not profile:
                errors.append('SKILL.md: unsupported frontmatter profile')
            else:
                frontmatter_name = profile[1]
                if root.name != frontmatter_name or frontmatter_name != SKILL_NAME:
                    errors.append(
                        f'SKILL.md name and package directory must both be {SKILL_NAME}'
                    )
                if not 1 <= len(profile[2]) <= 1024:
                    errors.append('SKILL.md: description must contain 1–1024 characters')
        if len(skill.splitlines()) > 200 or len(skill.encode('utf-8')) > 16000:
            errors.append('SKILL.md: exceeds entry budget (200 lines / 16000 bytes)')

    for label, text in texts.items():
        # Inline Markdown links only; reference-style links are not used here.
        for target in re.findall(r'\[[^\]\n]*\]\(([^\s)]+)\)', text):
            try:
                parsed = urlsplit(target)
            except ValueError:
                errors.append(f'{label}: unsupported link target')
                continue
            if parsed.scheme in {'http', 'https', 'mailto'}:
                continue  # Never contact remote endpoints.
            if parsed.scheme or parsed.netloc:
                errors.append(f'{label}: unsupported link target')
                continue
            dest_rel, _info, reason = resolve_local_path(
                root, PurePosixPath(label), parsed.path
            )
            if reason == 'escape':
                errors.append(f'{label}: link escapes package')
            elif reason == 'case':
                errors.append(f'{label}: link path has incorrect case')
            elif reason == 'missing':
                errors.append(f'{label}: broken link')
            elif reason:
                errors.append(f'{label}: unsupported or unreadable local link ({reason})')
            elif dest_rel is not None and parsed.fragment and dest_rel.suffix == '.md':
                dest_text = texts.get(dest_rel.as_posix())
                if dest_text is not None and unquote(parsed.fragment) not in anchors(dest_text):
                    errors.append(f'{label}: missing anchor: {target}')

    owners: dict[str, str] = {}
    for module in MODULES:
        text = texts.get(f'references/{module}.md', '')
        sections = list(re.finditer(r'^## (P\d+) — .+$', text, re.M))
        if not sections:
            errors.append(f'{module}: no check sections')
        for index, match in enumerate(sections):
            check = match[1]
            if check in owners:
                errors.append(f'Duplicate check: {check}')
            owners[check] = module
            stop = sections[index + 1].start() if index + 1 < len(sections) else len(text)
            body = text[match.end():stop]
            for field in ('Applies', 'Steps', 'Verify', 'Risks', 'Reverse'):
                if len(re.findall(rf'^- \*\*{field}:\*\*\s+\S', body, re.M)) != 1:
                    errors.append(f'{check}: expected one nonempty {field} block')
    if set(owners) != IDS:
        errors.append(f'Check coverage mismatch: missing={sorted(IDS - owners.keys())}, extra={sorted(owners.keys() - IDS)}')
    router = texts.get('references/routing.md', '')
    rows = re.findall(r'^\| (P\d+) \| [^|]+ \| ([\w-]+) \|$', router, re.M)
    if Counter(check for check, _ in rows) != Counter(IDS):
        errors.append('Router must list P01–P48 exactly once')
    for check, module in rows:
        if owners.get(check) != module:
            errors.append(f'Router module mismatch: {check} -> {module}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    for error in errors:
        print(f'ERROR: {error}')
    if errors:
        print(f'FAIL: {len(errors)} issue(s)')
        return 1
    print('PASS: required files, frontmatter, entry budget, local inline links, fences, and 48-check coverage')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
