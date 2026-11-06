# Observability playbook

Use existing tools first. New telemetry, external uploads, production profiling, and monitoring services require permission. URLs, query text, labels, traces, heap data, and prompts can contain sensitive information. Sample and redact at collection, not just in the final report.

## P18 — Distributed tracing

- **Applies:** latency crosses components and the critical path is unclear.
- **Steps:** 1) Instrument a narrowly scoped request/job path using existing facilities. 2) Propagate correlation context with safe identifiers across sync/async boundaries. 3) Bound sampling, retention, label cardinality, and collection overhead; exclude secrets and raw personal data.
- **Verify:** parent/child relationships, queue time, retries, dropped spans, clock interpretation, errors, and instrumentation overhead; avoid summing overlapping spans as elapsed time.
- **Risks:** privacy exposure, cost, high-cardinality overload, biased samples, and instrument-induced latency; tracing is evidence, not itself an optimization.
- **Reverse:** disable/remove the introduced instrumentation/export only; handle collected data using authorized retention/deletion policy.

## P30 — Real-user measurements

- **Applies:** supported users/devices differ from controlled lab conditions; includes browser RUM and equivalent native field signals.
- **Steps:** 1) Define a user-centered metric and privacy/consent boundary. 2) Collect minimal sampled events with release/device/network segmentation and bounded cardinality. 3) Select a meaningful window and compare traffic mix and deployment changes.
- **Verify:** metric definitions, sample count, collection loss, bot/background effects, errors, and consent behavior. For web, evaluate LCP, INP, and CLS where supported; use current product targets, not invented universal thresholds.
- **Risks:** surveillance, biased cohorts, expensive labels, misleading aggregate scores, and causal claims from uncontrolled correlation.
- **Reverse:** stop introduced collection and follow the approved data lifecycle; preserve only authorized aggregated evidence.

## P31 — Constrained-device testing

- **Applies:** users operate on limited CPUs, memory, networks, storage, or battery.
- **Steps:** 1) Choose supported representative targets and tasks. 2) Test release-like builds on real hardware when available; label simulation/throttling as an approximation. 3) Exercise cold/warm, intermittent connectivity, and larger inputs within safe device limits.
- **Verify:** task completion, input response, memory, errors, output correctness, and accessibility under constraints; record device, thermal state, runtime, and network profile.
- **Risks:** emulator mismatch, unrealistic throttling, overheating, and optimizing for one unrepresentative device. Do not perform destructive low-storage or battery tests on personal devices.
- **Reverse:** restore only test-applied limits/settings and remove owned fixtures; stop testing if device health or user data is at risk.

## P41 — Reproducible benchmarks

- **Applies:** a performance claim needs repeatable controlled evidence.
- **Steps:** 1) Define workload, inputs, output validity, environment, and primary metric before running. 2) Use an existing harness or an authorized minimal one; isolate setup only when the user's task excludes it. 3) Repeat/interleave runs, record variance, and bound duration/data/concurrency.
- **Verify:** result correctness, observable work not optimized away, clock resolution, release flags, warmup, cache conditions, sample count, and independent rerun procedure.
- **Risks:** unrealistic microbenchmarks, timer noise, compiler elimination, training on the benchmark, cherry-picked results, and accidentally testing a remote service.
- **Reverse:** stop owned benchmark processes and remove only approved generated fixtures; retain sanitized results and limitations even if the candidate loses.

## P42 — Performance regression gates

- **Applies:** a stable benchmark or artifact budget can reliably detect future regressions.
- **Steps:** 1) Start with stable structural budgets or representative benchmarks on controlled runners. 2) Set thresholds from variance and product goals, separating warnings from release blockers. 3) Version baseline/workload definitions and require review for baseline updates; measure gate runtime/cost.
- **Verify:** an intentional regression is detected, harmless noise does not cause frequent failures, cold/warm and platform conditions are explicit, and tests still verify correctness.
- **Risks:** flaky CI, gaming thresholds, stale baselines, long builds, and untrusted pull requests running expensive code or accessing secrets.
- **Reverse:** disable the specific unreliable blocker with documented review while keeping visibility; do not silently raise thresholds to hide a regression.
