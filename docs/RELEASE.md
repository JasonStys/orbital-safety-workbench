# Release and rollback runbook

1. Check account Actions storage first. Record live artifacts separately from the billing meter and caches. Do not delete any data without new user approval. This project's CI uses no Actions artifact uploads or caches.
2. Run all local gates, inspect the diff, verify no secrets/private files and refresh generated docs after formatting.
3. Push reviewed source to main; inspect actual Validation and CodeQL results at that exact commit. Do not call queued/in-progress jobs successful.
4. Only after passing checks, dispatch `Portable release` with a new version/tag. It creates/updates a **draft** release with per-platform portable ZIPs and SHA-256 files. Every bundle is smoke-tested before upload. A failed matrix leaves a draft, not a claimed usable release.
5. Check all matrix outcomes, download/verify checksums and publish the draft. Release storage is separate from Actions artifact storage; do not hide this distinction when reporting storage.
6. Source and bundles are unsigned/unnotarized. Do not imply a security audit, OS signature or mission certification. Users should not bypass OS warnings. Rebuild from reviewed source if necessary.

Rollback: mark an affected release as prerelease or draft, document the problem, and recommend the previous verified version. Do not delete archived evidence or rewrite published tags. Make a normal corrective commit/release. There is no forced auto-update or remote command channel.

The app installs no service, edits no system configuration and needs no elevation. Stop its own console with Ctrl+C. History files and exported reports are user-owned; removing a portable bundle must not delete those files automatically.
