# Validation record

Status: **passed and published**. Reviewed runtime revision: `e297c283c0cc5590886a9e2965eaa1525fe3301b`.

## Final hosted evidence — 2026-10-20

- [Validation 39488314899](https://github.com/JasonStys/orbital-safety-workbench/actions/runs/39488314899): **all eight jobs passed**, covering four scientific/runtime environments, the complete browser suite and three native packages.
- [CodeQL 39488314820](https://github.com/JasonStys/orbital-safety-workbench/actions/runs/39488314820): **both language analyses passed**; GitHub's code-scanning API returned **zero open findings**. Alerts were corrected, not dismissed.
- Follow-up documentation/inventory commits rerun these gates. README badges show current-head status; these immutable links preserve a specific tested runtime revision instead of a self-referential claim about this report's own commit. File-purpose, private-file exclusion and path-confinement regressions make the follow-up Python suite 90 tests; application runtime behavior is unchanged. The catalog reads only Git's nonignored file list and excludes private key/environment/history formats even if accidentally tracked.

| Gate                    | Observed result                                                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Python/runtime tests    | **87 passed in each environment**: Ubuntu Python 3.12/3.14, Windows 3.14, macOS 3.14                                                 |
| Coverage                | **99.25% combined statements/branches** on Python 3.14; all runtime modules included; 90% enforced floor on every matrix job         |
| TypeScript unit tests   | **16 passed**                                                                                                                        |
| Browser end-user checks | **18 passed**: six each in Chromium, Firefox and WebKit                                                                              |
| Accessibility/layout    | No axe WCAG2A/AA or 2.1AA violations in tested desktop/mobile states; no horizontal overflow at 390px                                |
| Fallback/privacy        | No-WebGL evidence remains usable; no external requests observed in that flow; blocked preferences remain usable                      |
| Portable app smoke      | Windows amd64, Linux x86_64 and macOS ARM64: actual executable historical SGP4 export, health, built website and scenario API passed |
| Static/style/contracts  | Ruff, strict mypy, strict TypeScript build, Prettier, source contracts and generated inventories passed                              |
| Dependency audits       | npm and hash-locked Python development graph: no known vulnerabilities reported at check time                                        |

The final local Python suite also passed all **87 tests with 99.25% combined coverage**. CI resolved runtime patch versions and images are recorded in the linked job logs. Automated accessibility/security checks are bounded evidence, not guarantees of universal accessibility or perfect security.

## Portable release evidence

The exact-commit-gated [release workflow](https://github.com/JasonStys/orbital-safety-workbench/actions/workflows/release.yml) smoke-tests every native bundle before draft upload. [Release notes](https://github.com/JasonStys/orbital-safety-workbench/releases) contain published source commits, workflow evidence and SHA-256 checksums. Bundles are unsigned/unnotarized portable apps, not signed installers; checksums do not constitute code-signing authenticity.

## Initial local checks — 2026-10-20

- Windows, Python 3.14.6, Node 24.18.1.
- 83 Python tests passed; combined statement/branch coverage 99.24% across all runtime modules.
- 16 TypeScript unit tests passed; strict Python and TypeScript checks passed at initial build.
- npm install audit: zero vulnerabilities in the resolved graph.
- Initial integration testing detected and corrected SQLite connection lifetime leaks (transaction contexts do not close connections). Warnings remain errors; none are suppressed to pass this test.
- Browser checks detected ambiguous status semantics, an ARIA label without a role and a test selector using wrapping-label text. Corrections were revalidated across all three engines.

## Completed local integration checks

- Chromium and WebKit: all ten original end-user tests passed (five per engine), including actual JSON downloads, scenario changes, cursor/playback, retry, stale requests, preference failure, axe scans and narrow-screen help/overflow checks.
- Firefox: all five original end-user tests passed outside the restricted Windows sandbox. The initial launch failed before any app code ran because Firefox could not access a Windows registry component in the sandbox; no OS protection or browser security setting was disabled. The identical assertions passed with normal process permissions.
- Windows amd64 frozen executable: historical SGP4 export, loopback health, built website and synthetic scenario API passed. Native bundle checksum generated; it is unsigned, not an installer or code-signing attestation.
- Additional explicit no-WebGL/external-request and HEAD-method regression tests are included for the final validation pass.
- Final three-engine suite: **18/18 passed**, including explicit no-WebGL and no external-request assertions. Final Python pass before the last CLI error-handling regression: **84/84**, combined coverage **99.25%**. GitHub's final run will record the added database-error regression too.
- Ruff, strict mypy, TypeScript production build, Prettier and generated source/documentation inventories passed. npm and the fully pinned Python development graph audits reported no known vulnerabilities at the time checked.
- Manual browser use verified synthetic Demo B at 907 seconds, visible units/frame/provenance and responsive controls. Screenshot is in `docs/images/workbench.jpg`.

Actions storage was checked first: billing meter reported 0.5/0.5 GB; live run artifacts 58,024,434 bytes, separate caches 15,203,216,587 bytes. Existing data was untouched. This repo's API showed **zero Actions artifacts and zero caches** after validation. Workflows use no artifact upload or cache actions; releases use separate Release asset storage.

## First hosted run and corrections

At source commit `6c9d48f`, [Validation 39487738897](https://github.com/JasonStys/orbital-safety-workbench/actions/runs/39487738897) passed the browser suite, Windows scientific tests and all three native builds/smoke checks. Linux/macOS inventory checks failed because Python `Path` sorting differs by platform. The generator now sorts explicit POSIX string keys; a mixed-case filename regression test checks portability.

[CodeQL 39487738893](https://github.com/JasonStys/orbital-safety-workbench/actions/runs/39487738893) ran successfully but reported two findings. They were corrected, not dismissed: download headers now use fixed allowlisted names rather than echo scenario/query strings, and expected Ctrl+C shutdown emits an explicit stop message instead of an empty exception handler. A header-injection regression rejects encoded CRLF parameters. The final hosted checks and zero-open-alert state are recorded above.

No physical orbit accuracy, collision probability, operational suitability or certification is claimed. See the scientific method and testing strategy for exact scope.
