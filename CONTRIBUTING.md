# Contributing

This package is an initial, not-yet-licensed publication candidate. Resolve licensing and contribution terms with the owner before submitting or redistributing contributions; do not assume that public visibility grants rights.

## Content conventions

- Keep SKILL.md small and platform-neutral. Use progressive loading rather than moving every detail into the entry point.
- Preserve P01–P48 identities and their router mapping. Discuss new IDs and update coverage checks before expanding the catalog.
- Every technical check needs `Applies`, ordered `Steps`, `Verify`, `Risks`, and `Reverse` blocks. Include boundaries and realistic failure cases, not unconditional prescriptions.
- Separate instructions from evidence: a suggested test is not a test result. Cite current version-specific sources when adding exact external claims.
- Prefer existing project facilities over new dependencies or infrastructure. Never introduce hidden network calls, installs, telemetry, or auto-execution.
- Keep operational content canonical in English. Update the Persian overview when the public behavior changes; do not create conflicting translated safety rules.
- Maintain relative Markdown links, UTF-8 text, short lines/sections where practical, and no secrets, user data, copied videos, or unlicensed assets.

## Validation

Review and run the optional standard-library scripts from the package root using your Python 3.10+ launcher:

```text
python scripts/validate.py
python -m unittest discover -s tests -v
```

Tests use temporary directories and do not call the network or execute target-project code. Python may create bytecode caches. The validator itself is read-only. Neither tool validates every factual claim or every AI host's behavior.

For workflow or permission changes, manually exercise the scenarios in examples: read-only mode, missing tools, irrelevant technologies, denied approvals, overlapping user changes, regression/recovery, and prompt-injection-like source text. Report what was actually tried and limitations.

## Review expectations

Explain the workload served, why existing guidance was insufficient, safety/compatibility implications, and how the change was checked. Do not bundle unrelated repository or dependency changes. A structural CI pass does not replace technical review.

Do not post secrets or customer traces in public issues. A private security-report channel must be established by the owner; none is represented as verified here. No automated commit, push, release, or maintainer action is authorized by these contribution instructions.
