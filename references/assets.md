# Assets and delivery playbook

Use for actual application artifacts and delivery paths. Browser-specific features stay browser-specific; native/CLI projects may only need dependency or artifact analysis. Check ownership and licenses before transforming or redistributing assets.

## P02 — Image formats and sizing

- **Applies:** images materially affect transfer, decode, memory, or export costs.
- **Steps:** 1) Inspect actual display dimensions, density, alpha, color profile, and consumers. 2) Generate non-destructive alternatives in supported formats; compare encoding/decoding costs. 3) Use responsive sizes and compatible fallbacks where supported; reserve dimensions.
- **Verify:** transferred bytes, visual fidelity, decode time, transparency, supported platforms, and saved/exported output; compare representative photos and graphics.
- **Risks:** lossy detail, broken transparency, unsupported decoders, slow encoding, increased build storage; format conversion is not automatically beneficial.
- **Reverse:** restore original asset references; retain originals and do not overwrite user uploads.

## P06 — Static content distribution

- **Applies:** public assets have geographic latency or origin-load problems. A CDN may already be provided by the host.
- **Steps:** 1) Measure target regions and cache behavior. 2) Reuse approved infrastructure, version URLs, and configure TLS/CORS/cache keys. 3) Exclude private responses; require approval for vendor, DNS, residency, or cost changes.
- **Verify:** cold/warm delivery in relevant regions, cache keys, cross-origin fonts/canvas if used, and publication of updated assets.
- **Risks:** stale deployments, cache poisoning, regional outages, data exposure, cost, and invalidation complexity.
- **Reverse:** approved origin fallback or prior distribution config; preserve versioned assets needed by existing clients.

## P09 — Transfer compression

- **Applies:** compressible data crosses a constrained transport; inspect existing proxy/client capabilities first.
- **Steps:** 1) Identify actual content types and sizes. 2) Enable negotiated compression at one appropriate layer. 3) Preserve cache variation and streaming flush behavior; avoid recompressing already-compressed media and consider compression side channels for secrets mixed with attacker-controlled content.
- **Verify:** real GET/request transfer size, content equality after decoding, encoding negotiation, CPU, latency, and streaming under the actual proxy.
- **Risks:** CPU pressure, buffering, incompatible clients, double compression, sensitive-length leakage.
- **Reverse:** restore compression settings for affected routes/assets; ensure cached encoded variants remain correctly identified.

## P11 — Unused dependencies

- **Applies:** dependencies create install, build, distribution, startup, or maintenance cost.
- **Steps:** 1) Inspect static/dynamic imports, plugins, configuration, side effects, optional and peer dependencies. 2) Obtain dependency-change authorization. 3) Remove through the project's manager and update the correct lockfile without unrelated upgrades.
- **Verify:** reproducible install in an approved isolated environment, build/tests, dynamic paths, plugins, supported platforms, and actual shipped artifact size.
- **Risks:** apparently unused packages may be runtime-loaded or required by tooling; removing a dev dependency does not necessarily shrink shipped code.
- **Reverse:** restore the specific manifest/lock changes and required package versions through the approved manager.

## P15 — Deferred image loading

- **Applies:** off-screen images compete with initial useful content.
- **Steps:** 1) Identify initial-viewport and likely LCP/critical imagery. 2) Defer only non-critical images with native lazy loading or existing platform support. 3) Reserve layout space and select a preload distance appropriate to scrolling/network speed.
- **Verify:** request timeline at startup and during fast scrolling; first critical image, layout stability, and images near the viewport remain timely.
- **Risks:** lazy-loading the hero worsens loading; overly late thresholds show blanks; eager prefetch defeats savings.
- **Reverse:** restore eager loading only where necessary, keeping dimensions and responsive sizing.

## P21 — Third-party scripts

- **Applies:** browser integrations block rendering or consume main-thread time.
- **Steps:** 1) Inventory necessity, consent requirements, network and execution cost. 2) Use async for independent scripts, defer for appropriate ordered scripts, or interaction/consent loading. 3) Preserve dependencies and essential failure fallbacks; do not weaken CSP for convenience.
- **Verify:** block or slow the vendor in a controlled test; core tasks still work; measure long tasks as well as download timing; verify required analytics/consent behavior.
- **Risks:** missed events, order races, broken authentication/widgets; async/defer do not eliminate execution cost.
- **Reverse:** restore only the integration timing/configuration changed, not unauthorized tracking.

## P22 — Code splitting

- **Applies:** users receive expensive code for unused routes/features; similar deferred modules may apply outside the browser.
- **Steps:** 1) Analyze the shipped dependency graph. 2) Split at meaningful feature boundaries using existing tooling. 3) Add loading/error/retry behavior and a version-compatible asset lifecycle; avoid excessive small chunks or eager prefetch of everything.
- **Verify:** initial bytes and parse/execute time, direct deep links, first feature use, offline behavior, and old clients after a release.
- **Risks:** request waterfalls, delayed first interaction, missing old chunks, broken synchronous contracts, module initialization order changes.
- **Reverse:** restore bundling/import boundaries and retain assets required by active clients until safe retirement.

## P27 — Client asset caching

- **Applies:** unchanged public resources are repeatedly transferred. Native caches need their own platform policy.
- **Steps:** 1) Separate content-hashed assets from mutable HTML/config and private data. 2) Assign appropriate expiry/revalidation; use long-lived immutable caching only for genuinely immutable URLs. 3) Inspect service workers and logout/account-switch invalidation.
- **Verify:** cold and warm visits with cache enabled, deployment updates, authenticated boundaries, offline/reconnection, and cache storage limits.
- **Risks:** stale critical fixes, private-content leakage, service-worker version conflicts, quota pressure; cache behavior cannot be inferred from headers alone.
- **Reverse:** restore affected policies/versioned manifests; invalidate scoped data if authorized, never blindly clear users' offline content.

## P29 — Font delivery

- **Applies:** font requests or rendering block usable text. Self-hosting needs an appropriate license and may not always be faster.
- **Steps:** 1) Inventory glyph coverage, weights, and licensing. 2) Compare approved self-hosting/subsetting/variable-font options by actual size. 3) Select display/fallback strategy; preload only proven critical files and preserve shaping rules.
- **Verify:** transfer and text visibility, layout shifts, fallback, CORS, supported scripts, RTL, numerals, combining marks, Persian half-spaces, and mixed-language text.
- **Risks:** missing glyphs, changed metrics, synthetic weights, broken ligatures, extra connections, and license violations.
- **Reverse:** restore licensed original files and references; keep all required language coverage.
