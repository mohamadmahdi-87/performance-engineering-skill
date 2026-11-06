# Cross-check interactions

Read when an experiment crosses layers or combines tactics. Keep one primary hypothesis; split changes when effects cannot be attributed. This is an interaction map, not another checklist to implement.

| Combination | Common failure | Required guardrail |
|---|---|---|
| Deduplication + cancellation (P03/P12) | One subscriber cancels shared work needed by others | Explicit ownership/reference counting or isolated subscriber cancellation |
| Debounce + requests (P04/P03) | Old response overwrites current input | Request generation/version check; IME and final-input tests |
| Pagination + joins + virtualization (P05/P08/P23) | Duplicate/missing rows, query expansion, inaccessible navigation | Stable ordering and identity; bound server work; focus/selection tests |
| Cache + optimistic writes (P10/P14) | False success or stale views survive a mutation | Versioned reconciliation and invalidation across affected views |
| Cache + permissions (P10/P27/P43) | Cached data crosses tenant or permission boundaries | Auth-aware keys and policy-specific invalidation; two-identity tests |
| Cache expiry + retries + replicas (P10/P38/P28) | Stampede multiplied across instances | Global capacity budget, jitter, bounded coordination, one retry owner |
| Compression + streaming (P09/P13) | Buffering delays first output; CPU becomes bottleneck | Test actual end-to-end proxies, flush behavior, and CPU |
| Lazy assets + initial rendering (P15/P20/P22/P29) | Critical image/font/code is deferred | Identify first useful path; avoid request waterfalls and over-preload |
| SSR + shared cache (P20/P10) | Personalized HTML is publicly cached | Separate public/private content and test identity isolation |
| Splitting + client cache + releases (P22/P27/P46) | Old clients request deleted chunks | Compatible immutable assets, staged retirement, offline/version tests |
| Parallelism + pooling + replicas (P16/P25/P28) | Aggregate connections exceed the database cap | Budget across all instances/workers and include queue wait |
| Background work + retries (P07/P38/P40) | Duplicate/lost work; queue delay hidden by fast acknowledgement | Durable handoff where required, idempotency, queue age, completion metric |
| Deadlines + mutations + retries (P12/P38/P39) | Timeout incorrectly treated as proof of failure | Outcome lookup/idempotency and bounded reconciliation |
| Index + writes + migration (P17/P39/P46) | Read gains cause lock/write/storage regressions | Approved migration rehearsal and write-path measurement |
| Edge + remote data (P19/P28) | Faster user-to-server hop but slower database path | Regional end-to-end and consistency measurements |
| Memoization + caches + memory (P26/P33/P34) | CPU savings create retention or stale state | Bounded cache lifetime, invalidation, repeated lifecycle tests |
| Fewer copies + buffer reuse (P33/P35/P44) | Aliasing, data leaks, corrupted output | Ownership and lifetime tests; zero/copy sensitive data as required |
| Streaming + parsing + quotas (P13/P40/P44) | "Streaming" library buffers the whole payload internally | Inspect actual behavior and enforce bounds during expansion |
| Fonts + virtualization + accessibility (P29/P23/P45) | Language coverage and navigation regress | Supported scripts, screen-reader, keyboard, print/export tests |
| Telemetry + benchmarks (P18/P30/P41) | Instrumentation overhead or sampling bias creates a false gain | Same instrumentation in A/B; low-overhead confirmation |
| AI prompt trimming + caching (P47/P10/P43) | Missing requirements or stale/cross-user answers | Quality set, versioned identity-aware cache, retained instruction hierarchy |
| Batching + accelerator + energy (P48/P37/P40) | Throughput improves while latency, VRAM, or energy worsens | Include queue delay, transfer, memory, and energy/cost per useful task |

## Shared-state questions

Before keeping the change, identify who else uses the resource: another tab, user, tenant, worker, process, replica, region, application version, or offline client. Test the relevant boundaries. A local happy-path test cannot establish distributed correctness.

If two experiments compete for the same budget, rerun the combined workload. Do not add independently measured percentage improvements together; their bottlenecks may overlap or move.
