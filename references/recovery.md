# Stop, recover, and hand off

A rollback plan is scoped evidence, not permission to undo arbitrary work. Code reversal, configuration rollback, cancelling execution, and recovering durable data are different operations.

## Immediate response

1. Stop the experiment on a correctness/security failure, budget breach, unexplained side effect, or sensitive output. Do not continue load to get a better sample.
2. Stop only processes/jobs/resources created by this run, using known identities and approved controls. Avoid broad process kills, global cache flushes, resets, or recursive deletion.
3. Capture minimal sanitized diagnostics: experiment ID, time/window, versions, symptoms, affected scope, and known in-flight work. Do not paste private payloads or secrets into reports.
4. Compare the current state with the recorded pre-change state. If other work overlaps, do not overwrite it. Preserve the user's diff and ask for coordination where permitted.
5. Decide whether scoped reversal is authorized and actually safe. If it is not, report needs-approval and a concrete containment/recovery plan. If questions are prohibited, record the blocker and stop the gated action.

## Recovery by change type

| Change | Safe response | Watch for |
|---|---|---|
| Local source only | Reverse exact owned edits after checking current diff; rerun relevant tests | User edits in the same region, generated artifacts |
| Timers/listeners/resources | Stop accepting new work; release only owned resources | Shared subscribers, queued callbacks, cancellation races |
| Dependency/config | Restore approved compatible manifest/lock/config state using project tooling | Install hooks, incompatible cached builds, other dependency edits |
| Cache | Bypass or invalidate scoped keys with an approved capacity plan | Origin overload, private data, old clients, irreversible offline loss |
| Jobs/streams | Drain, cancel, or reconcile by known job identity and durability contract | Already committed effects, duplicate delivery, partial output |
| Data/schema | Use tested restore/forward-repair plan with explicit data authority | New writes since backup, incompatible old versions, irreversible transforms |
| Deployment/region | Follow the operational owner's staged rollback or forward repair | Sessions, mixed versions, replication, DNS/cache delay |
| External data exposure | Stop the export and notify through the approved private channel | Credential rotation and retention/deletion need owner action; do not conceal evidence |

Never assume a reverse migration recovers deleted data. Never restore an old database backup over newer legitimate writes without an approved recovery plan. A feature flag can change future code paths, not undo completed side effects.

## Verify recovery

Re-run the narrow correctness check and, where authorized, the baseline workload. Confirm no orphan jobs, servers, temp files containing private data, or paid resources remain. Cleanup may itself require approval; report anything intentionally left running or retained.

Mark `reverted` only when the identified change was actually reversed; distinguish recovery tests passed, failed, and not run. If reversal is partial, state what remains and why. Do not call the environment restored without evidence.

## Blocked-run handoff

Record: safe stopping point, exact changed files/resources, last verified state, unresolved side effects, permission needed, sanitized evidence location, and next smallest action. Leave a plan rather than improvising a risky repair.
