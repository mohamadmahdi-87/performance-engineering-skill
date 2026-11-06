# Local package validation

## Observed results

- Host: Linux; Python 3.11.16.
- `python3 scripts/validate.py`: PASS.
- `python3 -m unittest discover -s tests -v`: 25 tests passed.
- Execution used `PYTHONDONTWRITEBYTECODE=1`; no dependencies were installed and no network access was needed by these checks.

The checks cover required package files, the intentionally restricted frontmatter profile, entry-point size, local inline Markdown links and simple heading anchors, fenced-block balance, unique P01–P48 sections, five required blocks per check, and router-to-module consistency. Mutation tests exercise failures as well as a valid package, CLI exit codes, and read-only validation.

## CI configuration, not observed execution

The GitHub Actions definition uses Linux, Windows, and macOS runners with Python 3.10 and 3.13 (six combinations), read-only repository permissions, a five-minute job timeout, disabled checkout credential persistence, and commit-pinned checkout/setup-python actions. It does not install application dependencies, deploy, or publish. GitHub's runner provisioning and action setup may use the network; the offline claim applies to the local validator and tests, not the entire CI service.

The workflow has not been executed on GitHub here. Windows/macOS, other Python versions, and AI-host integrations have not been tested in this session. Action pins are configuration choices, not a claim that their upstream code was security-audited or checked for latest versions.

## Boundaries

This is a package-specific checker, not a general YAML/Markdown parser. It checks inline links used in the package, not reference-style Markdown links or live external URLs. It does not parse GitHub workflow semantics, certify technical advice, audit secrets/Git history, benchmark target software, or guarantee that a model follows instructions. The metadata profile is deliberately fixed; changing metadata conventions requires updating the checker and tests.

No commit, push, release, deployment, or license grant was made. License selection and rights confirmation remain owner decisions. Package validation is not publication approval.
