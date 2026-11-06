# Changelog

## Unreleased

- Harden package validation against symlinks, Windows junctions, and Windows path-case ambiguity; require the package directory to match the skill name and validate `docs/VALIDATION.md`.
- Pin the multi-platform workflow to verified Node 24-compatible action commits and check out under the skill directory name.
- Document the distinct repository and skill names, clone command, ZIP folder name, and validator limits.

## 0.1.0 — Initial publication candidate

- Replace a monolithic web-performance guide with a selectively loaded Agent Skill.
- Preserve 31 original theme IDs and add 17 runtime, safety, measurement, and AI/compute checks.
- Add audit-first permissions, bounded experiments, measurement discipline, interactions, and recovery.
- Add English/Persian overviews, report/experiment templates, usage scenarios, provenance, and publication guidance.
- Add an optional offline package validator, regression tests, and a multi-OS CI definition.

No tagged/versioned release has been made. Licensing awaits owner selection. CI and host/platform compatibility must be reported from actual runs, not inferred from configuration.
