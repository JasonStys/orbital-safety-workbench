# Security and privacy model

## Protected boundary

The app handles only bundled public historical/fictional scenarios. It has no login, upload, remote catalog, URL fetch, external AI, arbitrary code execution or telemetry. It binds solely to `127.0.0.1`, not LAN/public interfaces. The Python standard-library HTTP server is used as a **local application transport**, not an Internet production server.

GET routes: `/`, allowlisted `/assets/<file>`, `/api/health`, `/api/catalog`, `/api/run`, `/api/report`. Mutating methods are refused. Parameters are finite/length-bounded, duplicates rejected, and the science cache contains only nine supported combinations. The server is not intended to resist a malicious process already running as the OS user or sustained local denial-of-service.

## Threats and controls

| Threat                                     | Control / test                                                                                                                       |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| DNS rebinding / foreign website access     | Exact single Host header with current loopback port; foreign Origin and cross-site Fetch Metadata rejected; no CORS                  |
| Source/hidden file disclosure              | Flat static-asset allowlist, resolved-path confinement (including symlinks), no percent/backslash paths or general directory serving |
| Script/markup injection                    | No user text input; dynamic UI uses textContent/typed numeric SVG; exported HTML is escaped and script-disabled                      |
| Unexpected resources, framing, advertising | CSP self-only scripts/styles/connections, frame-ancestors/object/form/base denied; all assets bundled; no ad/analytics scripts       |
| Spreadsheet formulas                       | Object-name cells starting with formula prefixes are neutralized in CSV; other free text is not imported                             |
| SQL injection / history corruption         | Parameterized values, transaction, schema constraints, immutable update trigger, run content hash validation                         |
| Stale misleading UI                        | Abort/generation protection, complete result replacement, explicit error with old-evidence notice, no operational labels             |
| Supply-chain updates                       | Hash-locked Python graph, npm lock, immutable Action SHAs, dependency audits, CodeQL, limited workflow permissions                   |

CSP is defense in depth, not a universal ad blocker or protection against compromised browsers, extensions, OS malware or a malicious repository maintainer. There is no promise of perfect security. A local administrator can inspect/change local files. No server operator receives data because no public service is deployed.

## CI and publication

PR validation has read-only contents access and does not expose repository secrets or use `pull_request_target`. CodeQL has only required security-event permissions. Native draft-release workflow is manual with contents write, protected by default-branch/ref checks and preceding verification. It does not execute an uploaded artifact. No Actions artifact/cache storage is consumed intentionally; code-scanning SARIF uses the separate security-analysis service.

## Reporting

Use GitHub private vulnerability reporting if enabled. Do not submit private data in public issues. Supply a minimal synthetic case, observed/expected behavior, version and affected path. No testing against real satellite control systems or unrelated networks is authorized by this repo.
