# Validation record

Status: local validation passed; publication and GitHub-hosted checks are pending. This document will be updated with exact hosted-run evidence before handoff.

## Initial local checks — 2026-10-20

- Windows, Python 3.14.6, Node 24.18.1.
- 83 Python tests passed; combined statement/branch coverage 99.24% across all runtime modules.
- 16 TypeScript unit tests passed; strict Python and TypeScript checks passed at initial build.
- npm install audit: zero vulnerabilities in the resolved graph.
- Initial integration testing detected and corrected SQLite connection lifetime leaks (transaction contexts do not close connections). Warnings remain errors; none are suppressed to pass this test.
- Browser checks detected ambiguous status semantics, an ARIA label without a role and a test selector using wrapping-label text. Corrections are being revalidated across engines.

## Completed local integration checks

- Chromium and WebKit: all ten original end-user tests passed (five per engine), including actual JSON downloads, scenario changes, cursor/playback, retry, stale requests, preference failure, axe scans and narrow-screen help/overflow checks.
- Firefox: all five original end-user tests passed outside the restricted Windows sandbox. The initial launch failed before any app code ran because Firefox could not access a Windows registry component in the sandbox; no OS protection or browser security setting was disabled. The identical assertions passed with normal process permissions.
- Windows amd64 frozen executable: historical SGP4 export, loopback health, built website and synthetic scenario API passed. Native bundle checksum generated; it is unsigned, not an installer or code-signing attestation.
- Additional explicit no-WebGL/external-request and HEAD-method regression tests are included for the final validation pass.
- Final three-engine suite: **18/18 passed**, including explicit no-WebGL and no external-request assertions. Final Python pass before the last CLI error-handling regression: **84/84**, combined coverage **99.25%**. GitHub's final run will record the added database-error regression too.
- Ruff, strict mypy, TypeScript production build, Prettier and generated source/documentation inventories passed. npm and the fully pinned Python development graph audits reported no known vulnerabilities at the time checked.
- Manual browser use verified synthetic Demo B at 907 seconds, visible units/frame/provenance and responsive controls. Screenshot is in `docs/images/workbench.jpg`.

Actions storage was checked first: billing meter reported 0.5/0.5 GB; live run artifacts 58,024,434 bytes, separate caches 15,203,216,587 bytes. Existing data was untouched. Workflows use no artifact upload or cache actions; releases use separate Release asset storage.

No physical orbit accuracy, collision probability, operational suitability or certification is claimed. See the scientific method and testing strategy for exact scope.
