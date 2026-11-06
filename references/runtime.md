# Runtime playbook

Applicable across runtimes when the workload exists. Use existing platform profilers and algorithms appropriate to the language/runtime; do not prescribe a shell, library, allocator, or concurrency model universally. Keep debug and release measurements distinct.

## P32 — Algorithms and data structures

- **Applies:** hot-path work grows poorly with input size or repeats avoidable computation.
- **Steps:** 1) Measure operation count and timing over realistic input sizes. 2) Identify complexity, constants, allocation, and locality. 3) Replace the narrow bottleneck with an appropriate algorithm/indexed structure while preserving ordering, equality, precision, and mutation semantics.
- **Verify:** trusted-reference comparison, empty/duplicate/adversarial inputs, realistic size scaling, peak memory, and small-input overhead.
- **Risks:** hash/equality mistakes, collision attacks, overflow, unstable order, extra memory, and a faster asymptotic algorithm that loses at actual sizes.
- **Reverse:** restore the original implementation behind the same contract; keep the new boundary/reference tests.

## P33 — Memory and allocation

- **Applies:** peak memory, garbage collection, allocator cost, or copying affects the chosen task.
- **Steps:** 1) Distinguish live data, retained capacity, allocations, resident memory, and runtime/OS caching. 2) Reduce unnecessary copies and lifetimes; use bounded reuse only when ownership is clear. 3) Profile realistic peaks, including encode/decode and failure paths.
- **Verify:** peak and steady-state memory plus CPU/latency; content correctness under reuse, concurrent operations, and large inputs.
- **Risks:** stale/sensitive data in reused buffers, aliasing, use-after-free in unsafe code, retained pools, recomputation, and worse locality. Forced GC is not a general fix.
- **Reverse:** restore simple ownership/allocation; remove only newly introduced pools/caches after users release them safely.

## P34 — Resource lifecycle and leaks

- **Applies:** resources accumulate across repeated operations or survive their owner unexpectedly.
- **Steps:** 1) Track lifetime and counts of listeners, timers, tasks, handles, sockets, file descriptors, object URLs, subscriptions, and native/GPU objects. 2) Pair acquisition with deterministic cleanup and defined ownership. 3) Cover exceptions, cancellation, partial initialization, and reentry.
- **Verify:** repeated create/use/dispose cycles after warmup, failure injection, and stable resource counts; a single growing heap sample does not establish a leak.
- **Risks:** premature cleanup breaks shared users; double-close, dangling callbacks, and finalizer dependence can introduce intermittent defects.
- **Reverse:** revert the scoped lifecycle change if it breaks ownership; retain leak evidence and add an ownership test before retrying.

## P35 — Filesystem and serialization I/O

- **Applies:** repeated reads/writes, serialization, copies, or synchronous I/O dominate the task.
- **Steps:** 1) Trace operation count/bytes and durability requirements. 2) Batch or stream bounded chunks using the existing format contract. 3) Preserve atomic replacement where supported, flushing requirements, error handling, permissions, encoding, and cross-platform path semantics.
- **Verify:** byte/semantic round trips, partial/truncated input, disk-full/permission failure, cancellation, large files, and recovery from interrupted writes in a sandbox.
- **Risks:** data loss from weaker durability, corrupt partial files, encoding changes, blocked UI/event loops, network-filesystem differences, and path traversal. Async APIs can still perform expensive CPU work.
- **Reverse:** restore compatible I/O behavior; recover durable files through backups/journals, never by deleting ambiguous originals.

## P36 — Startup and initialization

- **Applies:** startup, import, first request, or first interaction is too slow.
- **Steps:** 1) Separate process launch, dependency initialization, first useful output, and readiness. 2) Defer only non-critical work; remove repeated setup; use approved existing startup profiling. 3) Keep readiness honest and initialize shared state safely once.
- **Verify:** cold/warm launch, first feature use, concurrent first requests, failed initialization, supported deployment modes, and shutdown.
- **Risks:** shifting delay to a critical later interaction, partially initialized state, races, hidden connection errors, and false readiness.
- **Reverse:** restore initialization order/lifetime and clear only test-created state; never mask a startup failure by claiming readiness sooner.

## P37 — Resource budgets and energy

- **Applies:** constrained devices, container quotas, batch capacity, thermal limits, or operating cost matter.
- **Steps:** 1) Establish CPU, memory, disk, network, concurrency, battery/energy, and time budgets appropriate to the environment. 2) Reduce polling/wakeups and unnecessary work; make work resumable or yield where appropriate. 3) Use measured limits and existing quota controls, not arbitrary global tuning.
- **Verify:** representative devices/load, background/idle behavior, completion time, responsiveness, resource peaks, thermal state, and cost; use approved energy tooling or label CPU-based estimates as proxies.
- **Risks:** starving progress, draining battery through retries, thermal throttling, quota kills, and slower completion that increases total energy.
- **Reverse:** restore tested scheduling/limits; resume interrupted tasks safely and document any incomplete work.
