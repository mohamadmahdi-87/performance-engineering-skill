# Data playbook

Detect the actual engine and access pattern: SQL, document store, embedded database, IndexedDB, or another store. Do not translate every recommendation into SQL. No production query, schema change, or data migration is implicitly authorized; query-plan tools can execute real work.

## P05 — Bounded pagination

- **Applies:** a large collection is fetched or materialized without a meaningful bound.
- **Steps:** 1) Establish ordering, filters, and authorization. 2) Bound page size at the data source; choose stable keyset/cursor or offset semantics appropriate to mutations. 3) Return continuation/end information and handle cancellation; preserve the public API or obtain contract-change approval.
- **Verify:** first/last/empty/invalid pages, duplicates and omissions under concurrent mutation, tenant isolation, large inputs, and actual query work rather than just response size.
- **Risks:** unstable ordering, expensive total counts, deep offsets, cursor tampering, stale snapshots, broken consumers.
- **Reverse:** restore compatible contract/query behavior; do not reintroduce unbounded public access as an emergency shortcut.

## P08 — N+1 reads

- **Applies:** per-item related reads cause repeated remote/storage round trips.
- **Steps:** 1) Count calls at several collection sizes. 2) Batch keys or use a suitable join/eager-loading projection. 3) Preserve authorization, ordering, and null/missing relationships; bound batch sizes.
- **Verify:** call count growth, latency, returned data equality, memory, query plans, and pagination across small/large relationship counts.
- **Risks:** Cartesian expansion, huge batches, unnecessary relationships, connection contention, and per-request data mixed across users.
- **Reverse:** restore the prior access implementation locally; retain isolation tests and investigate a smaller batch rather than an unrestricted join.

## P17 — Query indexes

- **Applies:** measured query work can benefit from an index supported by the actual engine.
- **Steps:** 1) Inspect frequent predicates, joins, sorting, selectivity, existing indexes, and a safe query plan. 2) Design column/key order and estimate write/storage overhead. 3) Prepare an approved migration with engine-specific locking/online behavior and rollback limitations.
- **Verify:** representative data and actual plan use, rows/work examined, latency, write throughput, storage, and migration lock duration in an authorized environment. A small table may correctly use a scan.
- **Risks:** write amplification, prolonged locks, duplicate indexes, unique-constraint failures, and replicated/storage pressure. EXPLAIN ANALYZE may execute the query.
- **Reverse:** propose an approved index removal only after checking constraints and dependent plans; dropping can also lock and degrade performance.

## P24 — Minimal projections

- **Applies:** unused fields consume read, decode, network, or privacy budget.
- **Steps:** 1) Trace consumers and fields needed for identity, relationships, ordering, and continuation. 2) Project at the data source, not merely strip fields after loading. 3) Preserve response contracts or version an approved change.
- **Verify:** emitted query/projection, result equality for required fields, consumer tests, transfer size, and absence of sensitive fields from output/logs.
- **Risks:** hidden consumers, ORM lazy-load regressions, broken relationships, and unexpected follow-up queries that reintroduce N+1.
- **Reverse:** restore only required projections/fields; do not restore exposure of fields prohibited by security policy.

## P25 — Connection reuse

- **Applies:** connection setup or waiting is significant; inspect driver/framework pooling before adding another pool.
- **Steps:** 1) Measure active/idle connections and wait time. 2) Budget aggregate connections across replicas/workers, including serverless bursts. 3) Set bounded acquisition/idle lifetimes and ensure transaction/session state is reset on return.
- **Verify:** success/error/cancellation paths, leak-free release, connection recovery, pool saturation, and isolation of session state under bounded concurrency.
- **Risks:** exhausting server limits, stale connections, tenant state leakage, memory use, and long waits hidden behind a bigger pool.
- **Reverse:** restore tested limits/configuration with approved connection draining; avoid abruptly terminating unrelated transactions.

## P39 — Transactions and contention

- **Applies:** lock waits, conflicts, deadlocks, or serialized writes dominate a workload.
- **Steps:** 1) Inspect lock/wait evidence without exposing sensitive query values. 2) Shorten transaction scope and move independent expensive computation outside it while retaining atomic invariants. 3) Use consistent lock ordering or bounded, idempotent conflict handling; isolation/durability changes require explicit design review.
- **Verify:** concurrent writers, read-your-writes requirements, crash/timeout paths, deadlock recovery, no lost updates, and lock-time distributions under representative contention.
- **Risks:** shortened transactions can introduce races; lowering isolation or fsync guarantees can corrupt business semantics despite faster results.
- **Reverse:** restore the verified transaction boundary/configuration; reconcile any inconsistent data only through an approved recovery procedure.
