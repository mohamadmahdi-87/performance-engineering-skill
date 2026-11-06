# Routing and complete catalog

Read this lightweight index before detailed playbooks. Architecture is evidence; file extensions alone are not. Identify each executable component, its consumers, storage, runtime, and deployment boundary. Git, shell access, network, and package installation are optional, not assumed.

## Starting route

| Project/workload | Start with | Add only when present |
|---|---|---|
| Static site / browser application | interface, assets | runtime, services for remote calls; data only for actual storage |
| API / monolith / microservice | services, data | runtime, observability, safety-delivery |
| Mobile / desktop / game UI | runtime, interface | assets for actual delivery; services for network; safety-delivery |
| CLI / library / batch | runtime | data, services, ai-compute |
| AI application / inference / ETL | ai-compute, runtime | services, data, observability |
| Embedded / offline / constrained device | runtime, safety-delivery | data or interface only if present; domain expert for real-time/safety |
| Unknown / mixed monorepo | discover one workload first | do not load every module to compensate for uncertainty |

Native adapters: interpret rendering as the platform's UI update cycle, not a mandate for React. Interpret storage as its actual engine, not automatically SQL. Browser-specific techniques remain not-applicable on a non-browser surface. Platform profilers and measurements should come from existing project tooling; check exact version/API documentation before using unfamiliar commands.

No tools: reason from supplied evidence and output a plan. Read-only tools: static audit plus any explicitly permitted observational access. Local execution: bounded sandbox experiments after command review. Remote/production: scoped permission, resource limits, sanitized data, and rollback readiness are prerequisites.

## Catalog

Original 31 themes retain IDs P01–P31; additional themes are P32–P48. Titles are independently rewritten. A full audit must classify all 48 IDs, but can mark an entire absent capability group not-applicable using shared architectural evidence. Lack of runtime access is not proof of absence.

| ID | Check | Module |
|---|---|---|
| P01 | Loading placeholders | interface |
| P02 | Image formats and sizing | assets |
| P03 | Request deduplication | services |
| P04 | Debounced input | interface |
| P05 | Bounded pagination | data |
| P06 | Static content distribution | assets |
| P07 | Background work | services |
| P08 | N+1 reads | data |
| P09 | Transfer compression | assets |
| P10 | Application data caching | services |
| P11 | Unused dependencies | assets |
| P12 | Deadlines and cancellation | services |
| P13 | Incremental streaming | services |
| P14 | Optimistic interaction | interface |
| P15 | Deferred image loading | assets |
| P16 | Independent parallel work | services |
| P17 | Query indexes | data |
| P18 | Distributed tracing | observability |
| P19 | Compute/data locality | services |
| P20 | Pre-rendering strategy | interface |
| P21 | Third-party scripts | assets |
| P22 | Code splitting | assets |
| P23 | Large-list virtualization | interface |
| P24 | Minimal projections | data |
| P25 | Connection reuse | data |
| P26 | Redundant rendering | interface |
| P27 | Client asset caching | assets |
| P28 | Multi-instance capacity | services |
| P29 | Font delivery | assets |
| P30 | Real-user measurements | observability |
| P31 | Constrained-device testing | observability |
| P32 | Algorithms and data structures | runtime |
| P33 | Memory and allocation | runtime |
| P34 | Resource lifecycle and leaks | runtime |
| P35 | Filesystem and serialization I/O | runtime |
| P36 | Startup and initialization | runtime |
| P37 | Resource budgets and energy | runtime |
| P38 | Retry and idempotency policy | services |
| P39 | Transactions and contention | data |
| P40 | Backpressure and bounded queues | services |
| P41 | Reproducible benchmarks | observability |
| P42 | Performance regression gates | observability |
| P43 | Contract and version compatibility | safety-delivery |
| P44 | Untrusted input and storage limits | safety-delivery |
| P45 | Accessible and internationalized UX | safety-delivery |
| P46 | Release, migration, and recovery safety | safety-delivery |
| P47 | AI quality, latency, and cost | ai-compute |
| P48 | Compute/data-pipeline correctness | ai-compute |

Module files are directly linked from SKILL.md. Load by symptom, not catalog order. A focused run reports selected IDs and exclusions; an exhaustive run spends more context by design.

## Do not turn tactics into requirements

- No measured hot path: investigate before optimizing.
- No backend: do not add one for server-oriented checks.
- No database: no SQL/index/pool requirement; inspect local storage only if relevant.
- No network: CDN, retries, and remote telemetry are generally irrelevant.
- Already within agreed goals: a documented pass may be better than complexity.
- A functional or security defect discovered during profiling: report separately; prioritize safety without silently broadening implementation scope.
