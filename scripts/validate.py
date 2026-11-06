#!/usr/bin/env python3
"""Offline, read-only checks for this package; not a general Markdown/YAML parser."""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

MODULES = ('interface', 'assets', 'data', 'services', 'runtime',
           'observability', 'safety-delivery', 'ai-compute')
IDS = {f'P{i:02}' for i in range(1, 49)}
REQUIRED = (
    'SKILL.md', 'README.md', 'README.fa.md', 'CONTRIBUTING.md', 'CHANGELOG.md',
    'docs/PUBLISHING.md', 'docs/PROVENANCE.md', 'examples/scenarios.md',
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


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    if not root.is_dir():
        return [f'Not a directory: {root}']
    for name in REQUIRED:
        path = root / name
        if not path.is_file():
            errors.append(f'Missing required file: {name}')
    texts: dict[Path, str] = {}
    raw: dict[Path, str] = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            errors.append(f'Symlinks are not supported: {path.relative_to(root)}')
            continue
        if not path.is_file() or path.suffix != '.md':
            continue
        if not path.resolve().is_relative_to(root):
            errors.append(f'File escapes package: {path}')
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (UnicodeError, OSError) as exc:
            errors.append(f'{path.name}: cannot read UTF-8: {exc}')
            continue
        raw[path] = text
        texts[path] = unfenced(text, str(path.relative_to(root)), errors)

    skill = raw.get(root / 'SKILL.md', '')
    front = re.match(r'\A---\n(.*?)\n---(?:\n|$)', skill, re.S)
    if not front:
        errors.append('SKILL.md: missing YAML frontmatter delimiters')
    else:
        # Deliberately narrow: plain single-line name/description, then metadata.
        pattern = (r'name: performance-engineering\n'
                   r'description: ([^\n]+)\nmetadata:\n'
                   r'  author: ([^\n]+)\n  version: "(\d+\.\d+\.\d+)"')
        profile = re.fullmatch(pattern, front[1])
        if not profile:
            errors.append('SKILL.md: unsupported frontmatter profile or incorrect name')
        elif not 1 <= len(profile[1]) <= 1024:
            errors.append('SKILL.md: description must contain 1–1024 characters')
    if len(skill.splitlines()) > 200 or len(skill.encode('utf-8')) > 16000:
        errors.append('SKILL.md: exceeds entry budget (200 lines / 16000 bytes)')

    for path, text in texts.items():
        label = str(path.relative_to(root))
        # Inline Markdown links only; reference-style links are not used here.
        for target in re.findall(r'\[[^\]\n]*\]\(([^\s)]+)\)', text):
            parsed = urlsplit(target)
            if parsed.scheme in {'http', 'https', 'mailto'}:
                continue  # Never contact remote endpoints.
            if parsed.scheme or parsed.netloc or '\\' in target:
                errors.append(f'{label}: unsupported link: {target}')
                continue
            dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not dest.is_relative_to(root):
                errors.append(f'{label}: link escapes package: {target}')
            elif not dest.exists():
                errors.append(f'{label}: broken link: {target}')
            elif parsed.fragment and dest.suffix == '.md':
                if unquote(parsed.fragment) not in anchors(texts.get(dest, '')):
                    errors.append(f'{label}: missing anchor: {target}')

    owners: dict[str, str] = {}
    for module in MODULES:
        text = texts.get(root / f'references/{module}.md', '')
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
    router = texts.get(root / 'references/routing.md', '')
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
