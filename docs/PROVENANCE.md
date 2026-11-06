# Provenance and scope

## Content lineage

This package was developed from a prior Persian performance guide created in this conversation. That guide organized 31 themes visible in a user-supplied short video. Audio was unavailable; neither the prior guide nor this package is a verified audio transcript or an exact statement of the video's spoken advice.

P01–P31 preserve the original theme ordering, not verbatim prose. The operational instructions, risk analysis, permission model, recovery guidance, and examples in this package have been independently rewritten and expanded for a broader software context. Brand-specific suggestions are generalized: Redis becomes application data caching, OpenTelemetry becomes distributed tracing, and AI response streaming becomes conditional incremental streaming. No vendor adoption is mandatory.

P32–P48 are additional checks: algorithms, memory, lifecycle, I/O, startup, resource/energy budgets, retry/idempotency, transactions, backpressure, benchmarks, regression gates, compatibility, untrusted inputs, accessibility/internationalization, release safety, AI quality/cost, and compute correctness. These additions are not attributed to the video.

No source media, extracted frames, third-party diagrams, or target-project code/assets are included. The publisher should confirm any attribution obligations and rights before release. We do not invent the video's author or claim endorsement. Maintainer credit is Webzad (https://webzad.ir); legal ownership and licensing require owner confirmation.

## Format reference

The package layout and frontmatter follow the published [Agent Skills specification](https://agentskills.io/specification): a named directory with SKILL.md, YAML metadata, and selectively loaded references/assets. An external format reference is not a dependency or endorsement.

The local validator deliberately accepts a narrow frontmatter style suited to this package; it is not a general YAML implementation or an official certification. No experimental `allowed-tools` declaration grants implied execution permission. Host-specific installation directories and APIs are deliberately left to host documentation.

## Evidence and compatibility limits

Guidance is intended to transfer across operating systems and software architectures. That means capability detection and conditional tactics, not universal execution of the same commands. An assistant needs actual file and execution access to verify a target project; a text-only model can only reason about supplied evidence.

Source-level package validation does not establish behavioral compliance by every model, integration compatibility, security of a target project, speedup, or numerical token savings. Framework/provider/runtime-specific details and thresholds should be checked against the target's current version and actual product goals.

Safety-critical, medical, financial, hard real-time, and regulated systems require specialized review. This is performance-engineering guidance, not a legal, security, accessibility, or reliability certification.

## License boundary

No license was selected on behalf of the owner. No license from the earlier target application is inherited by this package. Choose and apply appropriate terms before offering licensed reuse; see the publication checklist. Third-party rights, if any, remain separate from any future license grant.
