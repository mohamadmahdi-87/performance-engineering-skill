# Performance report

Delete unused optional sections. Keep evidence short and sanitized. Never fill an unknown field with a guessed measurement.

## Contract

- Mode / depth:
- Workload and completion condition:
- Scope / exclusions:
- Environment, versions, build, input, cache state:
- Allowed actions / approvals / resource and time limits:
- Primary success criterion / guardrails:
- Evidence level: static / synthetic / representative / field

## Outcome

State what was found or changed, whether a benefit was measured, and the most important limitation. Distinguish source changes from deployed changes. Include the rollback state.

## Before / after

| Metric (unit and direction) | Baseline | Candidate | Difference | Runs / variability | Evidence |
|---|---|---|---|---|---|
| Primary | not measured | not measured | unknown | — | — |
| Correctness / errors | not tested | not tested | unknown | — | — |
| Resource / other guardrails | not measured | not measured | unknown | — | — |

Explain differences in environment, excluded samples, or uncertainty. No percentage without a meaningful nonzero baseline. Do not infer a percentile from a handful of runs.

## Check ledger

| ID | Status | Reason / observed scope | Evidence pointer | Next action / gate |
|---|---|---|---|---|
| selected ID | unknown | evidence missing | — | smallest safe next step |

Allowed statuses: `unknown`, `not-applicable`, `pass`, `needs-work`, `needs-approval`, `changed-unverified`, `verified`, `reverted`.

Focused: list selected IDs and explicitly exclude unreviewed IDs. Full: classify all P01–P48, with reason/evidence for each; absent capability groups may share architectural evidence. `verified` requires correctness and an evidenced outcome, not merely a modified file.

## Changes and tests

- Exact files/config/resources changed; public contracts affected:
- Tests/commands actually run, reviewed side effects, exit/outcomes:
- Checks not run and why; baseline failures versus new failures:
- New dependencies, external data, production access, migrations, commits, pushes, deployments: state actual actions, including none.
- Side effects, cost, compatibility, security/privacy/accessibility risks:
- Recovery performed/proposed; remaining resources and cleanup:

## Handoff / context checkpoint

- Last verified state and evidence pointers:
- Files/sections already read; existing user changes to preserve:
- Decisions and approvals with scope:
- Pending tests, blockers, next smallest experiment:
- Exact rollback boundary; uncertain data effects:
