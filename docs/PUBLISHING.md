# Publication checklist

This package is available in a public repository, but no tagged/versioned release or license grant has been made. No Git operations are part of package generation. Public visibility and an open-source license are separate decisions.

## Identity

- Repository name: `performance-engineering-skill`.
- Skill and package directory name: `performance-engineering`.
- Repository: `https://github.com/mohamadmahdi-87/performance-engineering-skill`.
- Description: `Evidence-first performance engineering skill for AI agents: modular audits, bounded experiments, regression checks, and safe rollback across software stacks.`
- Suggested topics: `agent-skills`, `ai-agents`, `performance`, `profiling`, `optimization`, `developer-tools`, `benchmarking`.
- Maintainer credit: Webzad — https://webzad.ir (credit is not a support SLA or a private security inbox).
- Version: `0.1.0`; maintain it in SKILL.md and the changelog when an actual release is authorized.

## Owner decisions before a licensed open-source release

- [ ] Confirm authorship/rights for the text and validation code and review provenance. Do not bundle the source video, frames, audio, or unrelated project assets.
- [ ] Choose a license and legal copyright holder. MIT is an option for permissive reuse, not a decision already made. Add the complete actual license text as `LICENSE`; update README license statements and optionally SKILL.md's `license` field. Do not publish a placeholder copyright holder/year as a real grant.
- [ ] Establish a genuine private reporting route if accepting security reports. Do not invent an email address or treat the maintainer's website as a verified confidential inbox. Until then, do not solicit sensitive details in public issues.
- [ ] Confirm the repository URL above is the intended public destination before linking to it elsewhere.

## Package checks

- [ ] Run `python scripts/validate.py` and `python -m unittest discover -s tests -v` with an available supported Python launcher.
- [ ] Optionally validate with the official `skills-ref` tool after reviewing and authorizing its installation; the local checker is not a replacement for the entire official validator.
- [ ] Review runtime instructions for unsupported universal claims and permission escalation.
- [ ] Review all files for private data, secrets, copied assets, and unintended local paths. A content review is not a full secret scan of Git history.
- [ ] Confirm P01–P31 remain mapped and P32–P48 are marked as additions in provenance.
- [ ] Review GitHub Actions pinned dependencies and runner/runtime policy when updating CI. Keep read-only permissions; do not add secrets to pull-request checks.
- [ ] Observe actual CI results before marking Windows/macOS/Linux support as tested. Record host/model smoke-test results separately from package validation.
- [ ] Test at least one tool-capable host and one manual/read-only usage path if claiming those integrations work. No behavioral smoke test is bundled as a universal model test.
- [ ] Run the manual scenarios in examples as relevant; verify selective loading, approval gates, no-tools behavior, and honest unknowns.

## Publish only with authorization

The repository already exists. Keep `SKILL.md` at its root and preserve references and assets. Do not upload unrelated workspace files. Clone the repository into the skill's required directory with:

```text
git clone https://github.com/mohamadmahdi-87/performance-engineering-skill.git performance-engineering
```

For ZIP downloads, rename the extracted package directory to `performance-engineering` before validation or installation.

Committing, pushing, tagging, changing visibility, enabling paid features, and releasing require the owner's authorization. Do not execute them merely because this checklist exists.

Release notes should distinguish: package checks actually run; host/OS/model combinations actually tested; CI configured versus observed; known limitations; and licensing status. Do not call the package universally compatible, zero-risk, or guaranteed to reduce tokens/performance costs.
