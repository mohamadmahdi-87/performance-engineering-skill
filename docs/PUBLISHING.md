# Publication checklist

This package is prepared for owner review, not already published or automatically licensed. No Git operations are part of package generation. Public visibility and an open-source license are separate decisions.

## Identity

- Repository/directory/skill name: `performance-engineering`.
- Description: `Evidence-first performance engineering skill for AI agents: modular audits, bounded experiments, regression checks, and safe rollback across software stacks.`
- Suggested topics: `agent-skills`, `ai-agents`, `performance`, `profiling`, `optimization`, `developer-tools`, `benchmarking`.
- Maintainer credit: Webzad — https://webzad.ir (credit is not a support SLA or a private security inbox).
- Version: `0.1.0`; maintain it in SKILL.md and the changelog when an actual release is authorized.

## Owner decisions before a licensed open-source release

- [ ] Confirm authorship/rights for the text and validation code and review provenance. Do not bundle the source video, frames, audio, or unrelated project assets.
- [ ] Choose a license and legal copyright holder. MIT is an option for permissive reuse, not a decision already made. Add the complete actual license text as `LICENSE`; update README license statements and optionally SKILL.md's `license` field. Do not publish a placeholder copyright holder/year as a real grant.
- [ ] Establish a genuine private reporting route if accepting security reports. Do not invent an email address or treat the maintainer's website as a verified confidential inbox. Until then, do not solicit sensitive details in public issues.
- [ ] Choose the actual repository URL and optionally add it to documentation. No fictitious clone URL is provided.

## Package checks

- [ ] Run `python scripts/validate.py` and `python -m unittest discover -s tests -v` with an available supported Python launcher.
- [ ] Optionally validate with the official `skills-ref` tool after reviewing and authorizing its installation; the local checker is not a replacement for the entire official validator.
- [ ] Review runtime instructions for unsupported universal claims and permission escalation.
- [ ] Review all files for private data, secrets, copied assets, and unintended local paths. A content review is not a full secret scan of Git history.
- [ ] Confirm P01–P31 remain mapped and P32–P48 are marked as additions in provenance.
- [ ] Review GitHub Actions pinned dependencies and runner/runtime policy before enabling CI. Use read-only permissions; do not add secrets to pull-request checks.
- [ ] Observe actual CI results before marking Windows/macOS/Linux support as tested. Record host/model smoke-test results separately from package validation.
- [ ] Test at least one tool-capable host and one manual/read-only usage path if claiming those integrations work. No behavioral smoke test is bundled as a universal model test.
- [ ] Run the manual scenarios in examples as relevant; verify selective loading, approval gates, no-tools behavior, and honest unknowns.

## Publish only with authorization

Use the owner's normal GitHub workflow to create/upload the repository contents. Keep SKILL.md at the repository root and preserve references and assets. Do not upload any unrelated files from the workspace. A fresh clone used as a skill should be in a directory named `performance-engineering`.

Creating a repository, committing, pushing, tagging, changing visibility, enabling paid features, and releasing are separately authorized operations. Do not execute them merely because this checklist exists.

Release notes should distinguish: package checks actually run; host/OS/model combinations actually tested; CI configured versus observed; known limitations; and licensing status. Do not call the package universally compatible, zero-risk, or guaranteed to reduce tokens/performance costs.
