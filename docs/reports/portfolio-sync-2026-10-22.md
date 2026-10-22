<!-- File: docs/reports/portfolio-sync-2026-10-22.md; Purpose: reviewed integration and validation trail by Jason Stys. -->

# Portfolio synchronization — 2026-10-22

## Follow-up dependency review

Dependabot created additional proposals after the first integration merged.
This separately validated follow-up retains their commit ancestry and reconciles
the complete dependency union rather than restoring an older package manifest.
Vitest and its coverage provider remain matched; current runtime and security
fixes are preserved. All native checks must pass on the new exact source head
before a normal merge. The earlier review below remains historical context.

By Jason Stys. Source baseline: `d42f8d7c945e873cda5c159276e51be9733b8b97`.

Reviewed original proposals: [#1](https://github.com/JasonStys/orbital-safety-workbench/pull/1), [#2](https://github.com/JasonStys/orbital-safety-workbench/pull/2), [#3](https://github.com/JasonStys/orbital-safety-workbench/pull/3), [#4](https://github.com/JasonStys/orbital-safety-workbench/pull/4), [#5](https://github.com/JasonStys/orbital-safety-workbench/pull/5), [#6](https://github.com/JasonStys/orbital-safety-workbench/pull/6). Their commit ancestry is retained in a combined integration candidate; a normal merge is permitted only after that exact candidate passes applicable native workflows. No branch protection, test threshold, security scan or failing step is bypassed. Historical references and intentionally separate experiments are preserved.

Dependency manifests are reconciled as the union of proposed dependency changes, not wholesale replacement with an older branch. Overlapping locks are mechanically resolved with the registry tools. Python package constraints and the actual installed CI/runtime locks are kept consistent; Vitest/coverage providers and CodeQL steps are coordinated. Runtime/data directories are not included in Git.

Validation is commit-specific: use this repository's [Actions](https://github.com/JasonStys/orbital-safety-workbench/actions) and integration PR checks. This record describes the reviewed work, not a claim that a future revision has already passed. Default-branch checks are verified again after merge. Private full audit and Actions backups stay on the owner's PC, outside public source.

The TypeScript major proposal is included for actual compatibility validation, not assumed compatible. CodeQL steps are pinned together and grouped. Civilian, non-guidance scope and scientific checks remain unchanged.
