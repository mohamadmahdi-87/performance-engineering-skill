# Performance Engineering

**A modular, evidence-first Agent Skill for diagnosing and improving software performance without sacrificing correctness or safety.**

[فارسی](README.fa.md) · [Skill entry point](SKILL.md) · [48-check catalog](references/routing.md) · [Publication checklist](docs/PUBLISHING.md)

Designed for web, backend, mobile, desktop, CLI, libraries, and AI/data workloads. The workflow is platform- and vendor-neutral; individual techniques are conditional. No tool, model provider, operating system, framework, package manager, or cloud service is mandatory for reading and applying the guidance.

**Status:** initial package, version `0.1.0`. Package structure can be validated locally. This is not certification that every host, model, OS, or target project works, and it does not guarantee faster or defect-free software. Licensing is an owner decision; see below before redistribution.

## What it does

- Starts in **audit** mode; edits and sensitive operations require scoped authorization.
- Locates one real workload and establishes a reproducible baseline.
- Selects relevant checks instead of loading an entire checklist into context.
- Plans bounded experiments, checks regressions and side effects, and defines reversal.
- Reports evidence, unknowns, blocked approvals, and untested conditions honestly.
- Covers **48 checks**: 31 original web-performance themes, generalized where valid, plus 17 cross-platform/runtime/safety/AI checks.

Each detailed check has **Applies → Steps → Verify → Risks → Reverse**. Architectural mismatches are not-applicable, not invitations to install extra infrastructure.

## Use it

### Get the package

The public repository is `performance-engineering-skill`; the skill name and required folder name are `performance-engineering`.

```text
git clone https://github.com/mohamadmahdi-87/performance-engineering-skill.git performance-engineering
```

For a ZIP download, rename the extracted package folder to `performance-engineering` before running the validator or installing it. Keep the full directory tree.

### In a skill-capable host

1. Keep the full package directory named **`performance-engineering`**; `SKILL.md` alone is not the complete skill.
2. Put the directory in the host's documented project/user skill location. Installation/discovery paths differ by host; no universal installation command is promised.
3. Enable/discover the skill using that host's documentation, then provide a workload, scope, permissions, and resource limits.
4. Let the agent load only the relevant references. Review its plan before authorizing changes.

The package uses the [Agent Skills format](https://agentskills.io/specification): YAML frontmatter plus Markdown, `references/` playbooks, and `assets/` templates. No experimental tool allowlist or platform-specific auto-execution hook is included. Host instructions and permissions always take precedence.

### With another assistant or a human

Open `SKILL.md` and `references/routing.md`, then the selected module. If the assistant cannot open files, supply those texts and the relevant measurement/workflow sections manually. Pasting only the entry point cannot magically expose linked files. Without runtime/tool access, request a static audit or plan, not a verified performance claim.

### Example requests

**Focused audit, no execution**

> Use performance-engineering in audit mode. Inspect the CLI CSV-import path only. Do not edit, execute scripts, access the network, or install packages. Identify at most three evidence-backed hypotheses and a bounded measurement plan. Mark missing evidence explicitly.

**Plan from measured evidence**

> Use plan mode for this API endpoint. Read the supplied redacted trace and relevant source. Compare pagination, N+1 reads, and projection options. Preserve the response contract. Do not execute database queries or modify files. Include failure cases and reversal.

**Authorized local experiment**

> Use implement mode for the already-approved local parser optimization only. Source and targeted test edits are allowed. After reviewing their side effects, run existing tests with synthetic fixtures: at most five minutes, one process, no network, no dependency changes, no production data, and no commits. Stop on unexpected resource use. Preserve output equality and report measured results or why measurement was blocked.

**Full audit**

> Classify all 48 IDs using available source evidence. No edits or commands. Use not-applicable only for demonstrated absent capabilities. Missing runtime evidence stays unknown; provide priorities rather than implementing all checks.

More scenarios: [examples](examples/scenarios.md).

## Architecture and context budget

```text
performance-engineering/
  SKILL.md                 Entry point: boundaries, loop, routing links
  references/
    routing.md             48 IDs and module selection
    measurement.md         Evidence and fair comparison
    workflow.md            Permissions and change workflow
    interface.md           Loading, interaction, rendering
    assets.md              Images, fonts, bundles, delivery
    data.md                Queries, indexes, connections, transactions
    services.md            APIs, caches, jobs, capacity, backpressure
    runtime.md             Algorithms, memory, I/O, startup, energy
    observability.md       Traces, field metrics, benchmarks, gates
    safety-delivery.md     Contracts, input limits, accessibility, release
    ai-compute.md          Quality/cost and compute correctness
    interactions.md        Cross-layer pitfalls
    recovery.md            Safe stopping and recovery
  assets/                  Report and experiment templates
  docs/                    Provenance and publication guidance
  examples/                Illustrative usage scenarios
  scripts/                 Optional offline package validator
  tests/                   Validator regression tests
  .github/workflows/       GitHub Actions package-check workflow
```

Ordinary runs load the entry point, router, and selected sections, **not** all reference files, translations, tests, and maintainer docs. Focused mode considers at most three candidate experiments. Each check has a stable ID for range reads and a compact evidence ledger. Full audits intentionally cost more context. Token counts depend on the host, tokenizer, retrieved context, and output; no fixed savings percentage is claimed.

## Safety boundaries

No silent deployment, commit/push, dependency installation, schema/data migration, paid service, external telemetry, production benchmark, or destructive cleanup. Permission to optimize source does not automatically authorize these actions. Commands and tests are reviewed for hooks, data writes, and network effects. Existing user edits must be preserved.

Performance gains must not weaken security, privacy, durability, correctness, accessibility, or supported contracts. Not every tactic improves every workload; each includes failure modes and reversal. Missing access produces a constrained report, not invented test results. Safety-critical and regulated domains need additional expert review.

## Validate this package (optional maintainer tools)

The skill itself is text-only. The optional validator requires **Python 3.10+**, standard library only, no network or installation. Review scripts before executing. From the package directory, using your platform's Python launcher:

```text
python scripts/validate.py
python -m unittest discover -s tests -v
```

Use `python3` or `py -3` instead if that is the installed launcher. The validator checks this package's intentionally restricted frontmatter profile, exact-case local inline links, symlinks/reparse points, the package-directory name, required files, unique coverage and structure for P01–P48, balanced fenced blocks, and entry-point size. It skips `.git` and never fetches external links. It is **not** a general YAML/Markdown parser, official specification certification, security audit, live-link checker, race-free filesystem guard, or model-behavior test.

Local results on November 6, 2026: the validator and 35 regression tests passed on Windows build 26300 with Python 3.14.7. Python 3.10/3.13 and the GitHub Actions run for this maintenance change had not yet been observed when this text was written. See [validation evidence and limitations](docs/VALIDATION.md). AI-host integrations have not been tested here.

The GitHub Actions workflow defines Linux, Windows, and macOS package checks with Python 3.10 and 3.13. A workflow file is not evidence of a successful run. Official `skills-ref` validation is a separate optional check described in the specification; it is not bundled or required at runtime.

## Repository identity

- **Repository name:** `performance-engineering-skill`
- **Skill and package directory name:** `performance-engineering`
- **Repository:** https://github.com/mohamadmahdi-87/performance-engineering-skill
- **GitHub description:** `Evidence-first performance engineering skill for AI agents: modular audits, bounded experiments, regression checks, and safe rollback across software stacks.`
- **Suggested topics:** `agent-skills`, `ai-agents`, `performance`, `profiling`, `optimization`, `developer-tools`, `benchmarking`
- **Maintainer credit:** [Webzad](https://webzad.ir)

The public repository contains the package, but no versioned release has been created. Repository visibility does not grant a license.

## Provenance and license

See [provenance](docs/PROVENANCE.md) for the distinction between the original 31 visual themes and newly authored guidance. No source video/audio, screenshots, project secrets, or third-party assets are distributed here.

**No license grant has been selected for this package.** Public visibility does not itself grant redistribution rights. The owner must confirm rights, choose a license, and add its actual `LICENSE` text before presenting this as licensed open source. MIT may be a suitable option if the owner intends permissive reuse, but it has not been applied on their behalf. The same decision must cover documentation and validation code. This skill does not change the license of any target project.

For contributions: [CONTRIBUTING.md](CONTRIBUTING.md). Before publishing: [docs/PUBLISHING.md](docs/PUBLISHING.md).
