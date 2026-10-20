# Test strategy

## Gates

- Python 3.12 and 3.14 on Ubuntu; 3.14 on Windows and macOS. Strict warnings, statement **and branch** measurement across every `orbital` runtime module; minimum 90%, no module exclusions.
- Fixed published SGP4 vector; native/pure portability across windows; bounded Hypothesis pair symmetry; single-object, endpoint, zero-relative-motion, between-sample minima and invalid fixtures.
- All nine scenario/window combinations; UTC historical anchoring, frame/units, finite samples, deterministic IDs and cache mutation isolation.
- Actual HTTP loopback socket tests: routes, origin/Host, no CORS, source/hidden/traversal paths, symlink resolution, long/duplicate/unreviewed queries, generic errors, refused mutations.
- JSON/CSV/escaped HTML; CSV formula defense; CLI no-overwrite; SQL idempotency, immutability, injection-as-data, hash rejection and 100-record cap. Resource warnings remain errors, including connection leaks.
- Ruff lint/format, strict mypy, TypeScript strict/noUncheckedIndexedAccess/exactOptionalPropertyTypes, Prettier and generated documentation drift checks.
- TypeScript pure display tests for endpoints, invalid offsets, constant chart scales, formatting and corrupt/blocked browser storage.
- Chromium, Firefox and WebKit against **the production Python handler and built website**, not a mocked UI backend. Scenario/window changes, object selection, slider/play/pause, real JSON download/parse, stale-request prevention, retry, localStorage failure, axe WCAG2A/AA+2.1AA scans and mobile overflow/help navigation.
- Native PyInstaller bundles on Windows/Linux/macOS: actual executable must export SGP4 evidence, serve health, built HTML and synthetic scenario API before packaging succeeds.
- Runtime and development dependency vulnerability audits, CodeQL Python/JavaScript-TypeScript analysis.

## Evidence integrity

Tests distinguish numerical verification, browser behavior, packaging and physical validity. Passing them does not validate current orbital positions or certify a safety product. Browser WebGL availability varies by host; fallback is part of the design. Automated accessibility testing does not replace assistive-technology user testing.

CI emits results to logs; it does not upload Actions artifacts or create Actions caches. Native ZIPs are uploaded only to a **draft GitHub Release** after a manually dispatched packaging workflow. Reports in `docs/reports/` record exact observed runs, environments, failures/remediations and residual limits. No result is called passed merely because a workflow file exists.

## Performance interpretation

Computations are bounded (≤8 objects/721 samples at the scientific contract, ≤3 objects in catalog). Complexity is documented in architecture. No unstable wall-clock CI threshold or claim of real-time operational throughput is used. The browser has no permanent animation loop while paused, caps pixel ratio to 2, updates markers without rebuilding line geometry and disposes GPU resources. Future performance changes should compare repeated cold/warm distributions on named hardware rather than one anecdotal duration.

## Reproduce

Use the README commands. On restricted Windows sandboxes, select a writable temporary directory with `TEMP`/`TMP`; for pytest an explicit disposable `--basetemp` under an existing `.runtime` directory also works. This is an environment accommodation, not a test skip or reduced assertion. Never disable OS security to run browsers or unsigned bundles.

For an already-running production service, set `ORBITAL_BASE_URL` to its printed loopback URL before browser tests. This avoids nested process ownership/teardown issues in restricted Windows shells while running the same assertions against the same handler. CI starts/stops its own isolated production service on Ubuntu by default.
