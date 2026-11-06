# Safety and delivery playbook

These checks constrain performance work; they are not a complete security audit, accessibility certification, or regulatory review. Never optimize away validation, isolation, durability, or compatibility. Report a newly found safety defect separately from measured performance gains.

## P43 — Contract and version compatibility

- **Applies:** optimizations affect public APIs, files, persisted state, exports, libraries, or supported runtime versions.
- **Steps:** 1) Inventory producers/consumers and documented compatibility guarantees. 2) Test old/new combinations and stable semantics including ordering, errors, locale, and precision. 3) Require approval for changed contracts; prefer additive/versioned transitions with explicit deprecation plans.
- **Verify:** golden fixtures or reference comparisons, backward/forward compatibility where promised, schema/version rejection, supported platforms, and mixed-version rollout behavior.
- **Risks:** apparently harmless size/timing changes can break clients, cache keys, signatures, or offline users; a passing current-version test misses older consumers.
- **Reverse:** restore compatible behavior only where stored/output formats allow it; use approved adapters or forward repair for irreversible changes.

## P44 — Untrusted input and storage limits

- **Applies:** imports, archives, images, documents, remote responses, or persisted records can exhaust resources or corrupt existing data.
- **Steps:** 1) Bound compressed/input bytes, entry count, per-entry and total expanded bytes, dimensions, nesting, time, and storage before or during expensive parsing. 2) Use parsers that enforce real incremental bounds; metadata and CRC are not decompression-bomb protection. 3) Validate paths/symlinks/types, reject collisions or remap identifiers consistently, and stage/commit atomically where supported.
- **Verify:** small synthetic boundary fixtures, malformed/truncated data, duplicate IDs, path traversal, cancellation, quota failure, and import/export round trips; previous records remain intact on failure. Do not generate huge hostile payloads.
- **Risks:** validation after full decompression is too late; hashes may require reading all data; ID overwrite can silently destroy unrelated assets; over-strict limits may reject legitimate work.
- **Reverse:** restore the verified parser/data path without removing necessary safety limits; recover affected records only from authorized backups or transaction rollback, not guessed reconstruction.

## P45 — Accessible and internationalized UX

- **Applies:** user-facing changes alter loading, timing, rendering, navigation, language, or input.
- **Steps:** 1) Preserve keyboard/focus, meaningful status/error announcements, reduced motion, and contrast. 2) Exercise supported locales, RTL, text expansion, shaping, IME/composition, and number/date rules. 3) Provide accessible alternatives for virtualized/deferred content and respect user preferences.
- **Verify:** relevant automated checks plus manual keyboard, assistive-technology, and language cases where available; state which combinations were not tested.
- **Risks:** silent progress/errors, focus loss, truncated translated text, inaccessible virtualization, broken font subsets, and flashing placeholders. A better timing score does not justify exclusion.
- **Reverse:** restore the prior accessible interaction/layout while keeping independent correctness fixes; do not remove accommodation to preserve a benchmark.

## P46 — Release, migration, and recovery safety

- **Applies:** an approved change will reach shared/production systems or alter durable formats/configuration.
- **Steps:** 1) Identify owner, rollout scope, approvals, monitoring, stop criteria, and tested restore procedure. 2) Review mixed versions, cache/chunk lifetimes, queue consumers, and schema compatibility. 3) Use the existing staged/canary/flag mechanism if appropriate; separate expand, migrate, and contract phases where needed.
- **Verify:** rehearsal with sanitized data, rollback/forward-repair feasibility, backup restoration, health indicators, draining, and explicit acceptance criteria; do not deploy merely to complete this check.
- **Risks:** irreversible migrations, stale clients, non-atomic multi-system changes, exposed flags, and backup files that cannot restore. Feature flags do not reverse data writes.
- **Reverse:** follow the approved release-specific plan; stop traffic/writes only with authority. If reversal risks data loss, escalate and use controlled forward repair rather than automatic rollback.
