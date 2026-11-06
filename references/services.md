# Services playbook

For actual remote calls, services, jobs, and shared caches. Adding Redis, queues, edge providers, or replicas is not a prerequisite. Prefer existing facilities; infrastructure changes remain approval-gated. Measure end-to-end completion, not just acknowledgement.

## P03 — Request deduplication

- **Applies:** equivalent concurrent reads repeat costly work.
- **Steps:** 1) Define equivalence including tenant/user scope, authorization, parameters, locale, and version. 2) Share only compatible in-flight work with bounded lifetime. 3) Remove entries on success/failure and define cancellation ownership; do not casually deduplicate writes.
- **Verify:** simultaneous equivalent and distinct requests, account changes, errors, cancellations, and retries; cancelling one subscriber must not unexpectedly cancel everyone.
- **Risks:** cross-user leaks, stale promise retention, swallowed errors, and unsafe mutation coalescing. In-flight deduplication is not durable caching or write idempotency.
- **Reverse:** restore separate calls and drain/remove only this mechanism's entries without disrupting other subscribers.

## P07 — Background work

- **Applies:** work can leave the foreground path without violating completion or durability contracts.
- **Steps:** 1) Distinguish accepted from completed. 2) Use existing approved workers with job identity, bounded queues, durable handoff where required, and status/error reporting. 3) Define retries, cancellation, deduplication, shutdown, and progress semantics.
- **Verify:** worker crash, duplicate delivery, rejection, queue full, reconnect, and restart; required jobs are not lost and effects are not duplicated.
- **Risks:** hidden failure, eventual consistency, queue growth, extra infrastructure, and misleading success UI; an unawaited promise is not a durable job system.
- **Reverse:** stop accepting new jobs into the changed path, drain/reconcile existing work, then restore the prior execution path with approval.

## P10 — Application data caching

- **Applies:** expensive reads repeat and an explicit freshness contract permits reuse.
- **Steps:** 1) Define cache keys with identity/authorization and data/schema versions. 2) Specify TTL, invalidation, negative-cache policy, size limits, and outage behavior. 3) Prevent stampedes with bounded coordination and jitter; use existing cache facilities where appropriate.
- **Verify:** hit/miss latency, memory, stale reads after mutation, logout/tenant isolation, concurrent misses, expiry, and cache failure. Measure origin load too.
- **Risks:** privacy leaks, stale permissions, inconsistent data, eviction churn, synchronized refresh, and extra cost. TTL alone may not satisfy correctness.
- **Reverse:** bypass the changed cache under a bounded origin-load plan; invalidate only affected keys if authorized, not an entire shared store.

## P12 — Deadlines and cancellation

- **Applies:** operations can wait indefinitely or outlive the requesting task.
- **Steps:** 1) Set an end-to-end deadline from the task budget. 2) Allocate remaining time across downstream calls, pool waits, and retries. 3) Propagate cancellation using real supported APIs and release resources; classify timeout separately from business failure.
- **Verify:** slow dependencies, connection stalls, cancelled callers, partial writes, and cleanup; server-side work actually stops where supported.
- **Risks:** aggressive deadlines create false failures; a timed-out mutation may have committed; merely racing a timer does not cancel underlying work.
- **Reverse:** restore the prior tested deadline policy, not unlimited waits; reconcile uncertain writes via status/idempotency rather than blindly retrying.

## P13 — Incremental streaming

- **Applies:** useful partial results can reach a consumer before full completion.
- **Steps:** 1) Define framing, encoding, ordering, and terminal/error states. 2) Verify actual proxy/client buffering and backpressure. 3) Bound chunk buffers and handle disconnect/cancellation; expose partial output only when safe.
- **Verify:** first useful output and full duration, slow readers, mid-stream errors, multibyte boundaries, integrity, and connection/resource cleanup.
- **Risks:** headers/status may be committed before failure; partial output may be unusable or unsafe; buffering can erase gains; open connections consume capacity.
- **Reverse:** restore the compatible buffered path after draining active streams; preserve error and output-integrity semantics.

## P16 — Independent parallel work

- **Applies:** a dependency graph contains independent operations and spare downstream capacity.
- **Steps:** 1) Prove independence, including side effects and ordering. 2) Choose a bounded concurrency limit using capacity evidence. 3) Define all-or-nothing versus partial results and cancel/collect remaining work on failure.
- **Verify:** completion time, peak memory, connection/pool waits, rate limits, output order, race behavior, and failure cleanup at the configured bound.
- **Risks:** race conditions, downstream overload, deadlocks, higher cost, and partial mutations; parallelizing everything can worsen tail latency.
- **Reverse:** restore prior scheduling or a lower verified limit; let in-flight work settle safely instead of duplicating it.

## P19 — Compute/data locality

- **Applies:** avoidable geographic or process-boundary round trips dominate latency.
- **Steps:** 1) Map users, compute, authoritative data, and transfer costs. 2) Compare co-location, batching, or existing regional capabilities before proposing edge execution. 3) Review consistency, residency, secrets, failover, and deployment ownership.
- **Verify:** representative regional latency, actual database round trips, cold starts, replication lag, cost, and failover behavior in approved environments.
- **Risks:** moving compute toward users but away from data makes requests slower; regional data copies add legal, consistency, and operational risks.
- **Reverse:** approved traffic routing to the previous compatible region; reconcile writes before retiring any replica or storage.

## P28 — Multi-instance capacity

- **Applies:** a measured capacity limit can be relieved by more instances; not a default cure for inefficient work.
- **Steps:** 1) Identify the saturated resource and serial/shared bottlenecks. 2) Review sessions, jobs, files, locks, migrations, and global connection budgets for multi-instance operation. 3) Propose approved load balancing/autoscaling bounds, health checks, and draining.
- **Verify:** capacity at bounded offered load, tail latency/errors, session continuity, instance loss, duplicate jobs, database saturation, and cost.
- **Risks:** shared-store overload, thundering herds, split state, oscillating scaling, larger bills, and duplicate singleton work.
- **Reverse:** approved scale-down with traffic/job draining and verified shared-state compatibility; do not abruptly remove active work.

## P38 — Retry and idempotency policy

- **Applies:** transient failures justify retrying an operation whose effects are understood.
- **Steps:** 1) Classify retryable failures and ambiguous outcomes. 2) Use a bounded attempt/deadline budget, backoff with jitter, and server retry guidance. 3) For mutations, use scoped idempotency keys and durable outcome/parameter checks where supported; choose one retry owner across layers.
- **Verify:** lost responses after successful writes, repeated keys with different payloads, expirations, rate limits, outages, and cancellation; count total downstream attempts.
- **Risks:** duplicate charges/writes, retry storms, delayed failure, and compounded retries across client/proxy/server. Backoff alone does not make a write safe.
- **Reverse:** reduce/disable the introduced retry layer while retaining valid operation identities and outcomes for outstanding requests.

## P40 — Backpressure and bounded queues

- **Applies:** producers can outpace consumers in queues, streams, workers, or in-memory buffers.
- **Steps:** 1) Measure arrival/service rates and queue age/bytes. 2) Bound count and memory plus per-tenant fairness. 3) Define safe rejection, blocking, shedding, or durable spill; connect admission control to capacity and expose overload clearly.
- **Verify:** short bursts, sustained overload within authorized test bounds, stalled consumers, cancellation, restart, and recovery; memory stays bounded and accepted durable work is accounted for.
- **Risks:** hidden data loss, starvation, deadlock, unbounded disk spill, and dropped critical tasks; larger buffers only postpone overload.
- **Reverse:** restore the prior safe admission policy or lower load; drain/reconcile accepted items before changing queue format or storage.
