# Workflow and approval gates

## 1. Discover without disturbing the target

Read project guidance, manifests, lockfiles, entry points, existing tests, and deployment notes relevant to the workload. Inspect the current diff/status if version control exists; otherwise record the exact files and safe recovery copies needed. Do not require a Git repository. Treat local configuration as sensitive; inspect only approved non-secret settings.

Identify OS, architecture, runtime/tool versions, target platforms, dependency manager, test commands, and actual storage. Record what is observed versus inferred. In a monorepo, distinguish the package from shared tooling before editing root configuration.

**Exit:** one workload, known boundary, permission envelope, available evidence, and exclusions. If these are unknown, continue discovery or deliver a constrained plan, not speculative edits.

## 2. Establish explicit bounds

Use the user's limits or choose a conservative proposal. If permission for execution is absent, do not execute. Bound duration, concurrency, input size, memory/disk, external requests, and monetary cost where relevant. For local timing experiments, start with small synthetic inputs; stopping on errors or resource pressure is mandatory. A production benchmark is never an implicit extension of a local test.

Review commands before running: package scripts, build plugins, install hooks, test fixtures, migration hooks, and shell expansion can have side effects. Avoid sudo/admin, global installs, curl-to-shell, credential prompts, public upload, and shell-specific assumptions. Use the approved project launcher for its platform; quote paths with spaces. Verify exact commands from the project rather than guessing npm, Bash, Docker, or Python.

## 3. Approval matrix

| Action | Required boundary |
|---|---|
| Read scoped non-sensitive source | Audit scope / host read permission |
| Run tests, profiler, build, benchmark | Execution scope plus reviewed side effects, sandbox/data target, and resource limits |
| Edit local source/tests | Implement scope; preserve user changes; define reversal |
| Change/add/remove dependencies or lockfile resolutions | Explicit dependency authorization; supply-chain and reproducibility review |
| Change public API, file format, persistence semantics, architecture | Explicit compatibility/design authorization |
| Access production, run load/fault tests, modify infra/DNS | Explicit target and action authorization; operational owner and stop conditions |
| Add telemetry/export data/use paid APIs | Explicit privacy, destination, and cost authorization |
| Apply migrations or alter durable user data | Explicit data-change authorization; backup/restore evidence and compatibility plan |
| Commit, push, release, deploy, rewrite history | Explicit operation-specific authorization; never implied by implement mode |

Existing explicit permission may satisfy a gate; do not repeatedly ask for the same action. Record its scope. If the user forbids questions, mark gated work needs-approval and finish what is permitted.

## 4. Prepare one experiment

Use the experiment template or a concise equivalent. Include:

1. Evidence locating the bottleneck, not merely a pattern match.
2. Hypothesis and minimal change. Name affected producers, consumers, configuration, and data.
3. Primary metric and success criterion chosen before observing the result; use product goals or a clearly labelled provisional target.
4. Guardrails: output equality/tolerance, security/isolation, errors, latency tails, memory, CPU, I/O, cost, accessibility, supported versions.
5. Test matrix: success, empty/boundary input, failure, cancellation, repeated/concurrent use, and upgrade as applicable.
6. Approval dependencies and remaining unknowns.
7. Exact scope of reversal. Code reversal and data recovery are different operations.

Prefer reducing unnecessary work before adding caches, services, concurrency, or architectural complexity. Do not bundle unrelated cleanup with a performance patch.

## 5. Apply and inspect

Change only the approved files. Preserve public contracts unless explicitly changing them. Avoid edits to generated files unless the generation source and process are understood. Keep lockfiles consistent through the correct manager when authorized. Add targeted regression tests near the changed behavior, not a new toolchain by default.

After editing, inspect the diff for unrelated modifications, accidental secrets, platform assumptions, and expanded permissions. If another actor changed the same region, stop and reconcile rather than overwrite. Record edits in the ledger without committing them.

## 6. Validate, decide, hand off

Run the targeted correctness tests first, then comparable measurements, then the relevant broader checks. A failed baseline test must be distinguished from a new failure; do not claim all failures are pre-existing without evidence.

- Benefit and guardrails supported: verified for the tested scope, not universally.
- Correctness passes but runtime unavailable: changed-unverified; state this before handoff.
- No material benefit / cost exceeds benefit: recommend reversal or justify non-performance value separately.
- Safety/correctness regression: stop the experiment; use the recovery playbook. Never retain a faster wrong answer.

Leave no orphan benchmark processes, temporary servers, containers, test users, or charged jobs. Clean up only resources created by this run and safe to remove. Record any cleanup that needs permission. Hand off exact test results, limitations, rollback state, and operational follow-up. A source patch is not a production rollout.
