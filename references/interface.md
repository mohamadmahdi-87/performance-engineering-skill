# Interface playbook

Read only checks relevant to the selected interaction. UI examples are conditional: use the native platform's equivalent where meaningful, not web libraries in every project. Shared permission and measurement rules remain in SKILL.md. `Reverse` means a scoped, authorized reversal, never overwriting other work.

## P01 — Loading placeholders

- **Applies:** asynchronous content leaves a confusing blank surface. Not a download-speed fix.
- **Steps:** 1) Identify actual wait states. 2) Reserve final content dimensions and add a simple placeholder. 3) Provide completion, empty, error, timeout, and retry states; avoid repetitive screen-reader announcements and honor reduced motion.
- **Verify:** test slow success, immediate cached success, error, and cancellation; placeholder disappears correctly; layout stays stable and focus is preserved.
- **Risks:** extra rendering, flashing, hidden errors, and indefinite waiting; animation can consume energy or impair accessibility.
- **Reverse:** restore the prior loading component without touching data-fetch semantics. Keep useful error handling if independently justified.

## P04 — Debounced input

- **Applies:** repeated non-critical input triggers expensive work. Avoid delaying safety-critical or immediate feedback.
- **Steps:** 1) Separate input updates from expensive requests. 2) Choose a measured delay, not a universal constant. 3) Cancel obsolete work or ignore stale responses; clean up timers on disposal; preserve Enter, clearing, and composition/IME behavior.
- **Verify:** deterministic timer tests plus rapid typing, out-of-order responses, clearing, navigation, and composed text; final intended input is processed exactly as required.
- **Risks:** increased perceived delay, lost final action, stale results, and language-specific bugs. Debounce does not replace rate limits.
- **Reverse:** restore dispatch timing and remove only added timers/cancellation wiring; preserve input state.

## P14 — Optimistic interaction

- **Applies:** reversible operations with a reliable reconciliation strategy, such as a preference toggle. Not proof of payment, authorization, or completed export.
- **Steps:** 1) Model pending state separately from confirmed data. 2) Assign operation identity/version. 3) Apply optimistic state, reconcile authoritative success, and restore/rebase on failure. Explain failure accessibly.
- **Verify:** rejection, timeout, repeated clicks, multiple tabs, and responses arriving in reverse order; an old rollback must not erase a newer action.
- **Risks:** false success, duplicate mutations, stale cache, and divergence across devices. Pair with P38 when retries are possible.
- **Reverse:** use server-confirmed UI updates again; reconcile outstanding operations rather than dropping them.

## P20 — Pre-rendering strategy

- **Applies:** browser routes where earlier useful HTML matters. SSR/SSG are not native-app or CLI requirements.
- **Steps:** 1) Classify static/public, dynamic, and personalized routes. 2) Compare current rendering costs with the existing framework's prerender options. 3) Define freshness, hydration, authorization, and cache boundaries; seek approval for architectural changes.
- **Verify:** initial HTML, useful paint, server latency, interaction readiness, direct navigation, hydration errors, and isolation between users. Test without JS only where that is an intended contract.
- **Risks:** server load, slow TTFB, hydration overhead, stale builds, and private-content leaks. SEO gains do not establish runtime gains.
- **Reverse:** route traffic back to the compatible previous rendering path; invalidate only affected caches under an approved rollout plan.

## P23 — Large-list virtualization

- **Applies:** large rendered collections cause measured layout/render/memory cost. Data pagination is a separate concern.
- **Steps:** 1) Measure node/view count and frame cost. 2) Render a bounded viewport with stable keys and measured overscan. 3) Handle dynamic heights, selection, keyboard navigation, focus, and assistive technology; plan print/export and find-in-page behavior.
- **Verify:** long lists, quick scrolling, resize, insertion, reorder, search, and keyboard focus; memory and rendered view count remain bounded.
- **Risks:** jumping content, lost focus, inaccessible off-screen rows, incomplete printing, and excessive bookkeeping for small lists.
- **Reverse:** restore the previous renderer or approved paginated fallback while keeping selection and scroll position meaningful.

## P26 — Redundant rendering

- **Applies:** profiler evidence shows expensive unnecessary UI updates. Frequent cheap updates alone are not a defect.
- **Steps:** 1) Identify the trigger and expensive subtree. 2) Narrow state ownership/subscriptions and remove redundant derived state. 3) Memoize only proven costs with correct dependency and lifetime semantics.
- **Verify:** update duration and task responsiveness, not just render count; test changing every relevant input, navigation, and repeated mount/disposal.
- **Risks:** stale closures, skipped required updates, memory retention, complex dependency rules; development double-invocation may not reflect release behavior.
- **Reverse:** remove the specific optimization and restore straightforward data flow; retain tests exposing stale-state defects.
