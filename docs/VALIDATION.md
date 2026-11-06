# Local package validation

## Previous audit results (before the maintenance pass)

### Observed results

- Host: Linux; Python 3.11.16.
- `python3 scripts/validate.py`: PASS.
- `python3 -m unittest discover -s tests -v`: 25 tests passed.
- Execution used `PYTHONDONTWRITEBYTECODE=1`; no dependencies were installed and no network access was needed by these checks.

The checks cover required package files, the intentionally restricted frontmatter profile, entry-point size, local inline Markdown links and simple heading anchors, fenced-block balance, unique P01–P48 sections, five required blocks per check, and router-to-module consistency. Mutation tests exercise failures as well as a valid package, CLI exit codes, and read-only validation.

## CI configuration, not observed execution

The updated GitHub Actions definition uses Linux, Windows, and macOS runners with Python 3.10 and 3.13 (six combinations), read-only repository permissions, a five-minute job timeout, disabled checkout credential persistence, `actions/checkout` v7.0.1 pinned to `3d3c42e5aac5ba805825da76410c181273ba90b1`, and `actions/setup-python` v7.1.0 pinned to `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0`. Both pins use Node 24. It checks out the repository into `performance-engineering` so the validator's package-name check sees the skill directory, while keeping the workflow at repository root. The configured matrix uses GitHub-hosted runners; self-hosted runner compatibility is not asserted. It does not install application dependencies, deploy, or publish. GitHub's runner provisioning and action setup may use the network; the offline claim applies to the local validator and tests, not the entire CI service.

The result for the maintenance commit is pending until that exact commit's GitHub Actions run is observed. Windows/macOS and Python 3.10/3.13 results must be read from those six jobs; configuration alone is not execution evidence. Pinning identifies exact upstream action revisions but does not mean their source was security-audited. AI-host integrations are not tested by this workflow.

## Boundaries

This is a package-specific checker, not a general YAML/Markdown parser. It checks inline links used in the package, not reference-style Markdown links or live external URLs. It requires exact path-component spelling even on case-insensitive filesystems, rejects symlinks and Windows reparse points rather than following them, skips `.git` (including case aliases) before inspecting it, and requires both the frontmatter name and package-directory basename to be `performance-engineering`. Its frontmatter profile is deliberately fixed; changing metadata conventions requires updating the checker and tests. These checks do not provide race-free protection if another process changes the filesystem during validation. The validator does not parse GitHub workflow semantics, certify technical advice, audit secrets/Git history, benchmark target software, or guarantee that a model follows instructions.

The statement that no commit or push was made describes the earlier audit only. License selection and rights confirmation remain owner decisions. Package validation is not publication approval.

## Maintenance execution (2026-11-06; before the updated workflow run)

- Host: Windows build 26300; Python 3.14.7, 64-bit. Python 3.10 and 3.13 were not installed locally.
- `python -B scripts/validate.py`: PASS, exit code 0; elapsed 0.237 seconds.
- `python -B -m unittest discover -s tests -v`: PASS, 35 passed, 0 failed, 0 skipped; exit code 0; elapsed 3.187 seconds (the unittest runner reported 2.784 seconds).
- Python 3.14.7's parser accepted both changed Python files with `ast.parse(..., feature_version=(3, 10))`. This checks grammar compatibility; it is not execution on Python 3.10.
- The local run exercised file and directory symlinks and a Windows junction. Instrumentation confirmed the validator did not enumerate the external directory target; the file-link test confirmed it did not read the external file target.
- The GitHub Actions run for the maintenance commit had not yet been observed when this record was written. No result is inferred from the workflow definition.
- No packages were installed. Raw stdout/stderr and result metadata were saved outside the repository for this maintenance pass.
