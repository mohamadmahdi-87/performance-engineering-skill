# One experiment

- **ID / selected checks:**
- **Contract:** mode, workload, scope, environment, allowed actions, time/resource/cost caps.
- **Observed bottleneck:** evidence pointer and evidence level; unknowns.
- **Hypothesis:** changing X should improve Y for workload Z because of observed cause W.
- **Minimal change:** exact components/files; producers/consumers and existing user work.
- **Primary metric:** unit, direction, predeclared success criterion.
- **Guardrails:** correctness, security/isolation, accessibility, errors/tails, CPU/memory/I/O/cost, compatibility.
- **Baseline:** input, build/runtime, cold/warm, concurrency, measurement method, runs and variability.
- **Test cases:** success; empty/boundary; failure; cancellation; repeated/concurrent; upgrade/old consumer, as applicable.
- **Interaction risks:** related IDs; shared resources; explain skipped cases.
- **Approval gates:** required, satisfied, or blocked; no implied production permission.
- **Stop conditions:** bounded budget, new errors, sensitive output, resource pressure, out-of-scope effects.
- **Reversal:** exact owned edits/resources; in-flight work; data reversibility; authorization and recovery verification.
- **Results:** correctness first, then comparable before/after; include unsuccessful runs and limitations.
- **Decision:** keep / revert / propose / blocked; status and evidence, not a guaranteed benefit.

Use this as a short record, not a requirement to duplicate the complete report. Keep large raw traces outside the agent context in an authorized redacted artifact location.
