# Measurement contract

## Choose the workload and metric

Measure a user or system task with representative input and a known completion condition. Primary metric examples:

| Workload | Primary candidates | Mandatory companion checks |
|---|---|---|
| Web interaction | LCP, INP, CLS, task completion | errors, transferred bytes, JS CPU, accessibility |
| API / service | latency distribution, throughput | errors/timeouts, saturation, offered load, cost |
| CLI / batch | wall-clock, records/second | output equality, peak memory, disk and CPU |
| Mobile / desktop | startup, frame timing, interaction | energy/thermal conditions, memory, foreground/background |
| Database | query latency, work/rows examined | writes, locks, connection wait, consistency |
| AI / compute | useful-first-output, total latency, cost/task | quality, determinism/tolerance, failures, memory |

Do not optimize a proxy while the actual task becomes slower. Distinguish startup, steady state, perceived progress, first byte, first useful output, and completion. A faster acknowledgement does not mean a faster finished job.

## Capture a reproducible baseline

Record code revision or file/diff identity, configuration (redacted), OS/architecture/runtime, hardware or simulator, build mode, dependencies, input shape/size, tool version, clock method, and competing workload. Use monotonic timing for elapsed durations where possible. Specify concurrency, offered load, cache/JIT warmup, cold/warm state, and network conditions.

Use sanitized representative fixtures. If production data is needed, request approved access rather than copying it locally. Protect profiler outputs: URLs, SQL, stack traces, and heap snapshots may contain secrets or customer data.

For exploratory local timings, start with at least three comparable measured runs when feasible, report median and range, and state that this is weak evidence. More repetitions and controlled ordering are needed for noisy/small effects. Never infer a reliable p95 from three samples. Do not silently discard slow runs; record exclusions and reasons fixed independently of desired results.

For service/field percentiles, record sample count, window, traffic mix, errors, and collection method. Separate p50/p95/p99 and throughput from averages; do not average percentiles across hosts as if they were raw samples. Include timed-out/failed requests in outcome accounting, not only successes. For load tests, record whether load is open-loop or completion-driven; a client that stops sending while the server stalls can hide overload. Ramp only within authorized limits.

## Compare fairly

Keep inputs, build mode, instrument overhead, hardware, dependency versions, and cache conditions comparable. Warm up JIT/caches deliberately when measuring warm behavior. Measure cold behavior separately; do not clear shared production caches to manufacture it. For short timings, use a harness that avoids timer-resolution noise without hiding setup or teardown costs relevant to the user.

Interleave or alternate baseline/candidate runs when environmental drift matters. Report absolute difference, relative difference, and variability. Label direction: a lower latency is better; a higher throughput may only be better if error and latency guardrails hold. If the baseline is zero or noise dominates, do not invent a percentage or statistical confidence.

Recheck downstream bottlenecks: faster enqueueing can grow queue age; lower bandwidth can increase CPU; lower memory can increase recomputation; batching can worsen tail latency. Compare both typical and large/boundary workloads. If small and large inputs behave differently, report both.

## Evidence levels

- **Static observation:** source/config/plan supports a hypothesis; no runtime performance claim.
- **Synthetic experiment:** controlled reproduction; applicability to production is limited.
- **Representative local/staging result:** known test workload and environment; still not a production guarantee.
- **Field evidence:** actual supported population and window; confounding changes must be disclosed.

A score or trace without conditions is not a benchmark. A profiler may perturb execution; verify important gains with lower-overhead measurements. Missing tools: record what cannot be measured and propose an exact future test. Do not install or upload artifacts without authorization.

## Stop conditions

Stop on a preset budget, unexpected external traffic, rising error rates, resource pressure, battery/thermal risk, sensitive output, loss of data integrity, or effects outside the test sandbox. Preserve only sanitized diagnostic evidence; terminate only your own jobs. Use the recovery playbook before attempting further changes.
