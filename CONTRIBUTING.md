# Contributing

Keep this a civilian educational replay/evidence tool. No operational targeting, intercept guidance, destructive models or spacecraft command interfaces.

- Prefer explicit units, frame and epoch in interfaces. Validate finite values and bounds before computation. Never fabricate uncertainty or convert an unavailable probability to zero.
- Use descriptive domain names and small focused functions. Document contracts, parameter/variable roles, failure behavior and scientific assumptions; explain important decisions rather than narrating obvious syntax.
- Each authored code file needs a responsibility/creator header pointing to `docs/CODE_INDEX.md`. Python functions/classes require docstrings. Keep web functions/methods documented. Run formatters **before** refreshing the generated exact-line definition/variable/file catalogs.
- Add reproducible reference/analytic/regression tests for every scientific change and a browser regression for visible behavior. Use synthetic/public fixtures, no private files or accounts. Never weaken tests, warning policies or thresholds to hide a failure.
- Record Big-O complexity and measured trade-offs. Prefer clear bounded algorithms and vetted scientific libraries to unnecessary languages or wrappers. Separate algorithm verification from physical accuracy claims.
- Lock dependencies with hashes/integrity; pin Actions to reviewed commits. Run audits and security analysis. Avoid unrelated dependency major upgrades without compatibility evidence.
- Check Actions billing/storage before dispatching checks. Use no artifact/cache uploads in this repo. Cleanup needs explicit user approval. Keep private PC archives out of Git.
- Follow the README validation commands, refresh `docs/reports/VALIDATION.md` with actual evidence and inspect CI at the exact proposed commit. Do not claim safety certification or universal compatibility.
