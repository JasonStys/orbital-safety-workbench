# Architecture and decisions

## Data flow

Reviewed built-in fixture → bounded scientific run → canonical JSON → loopback API → browser render/export.

The CLI can also save that evidence to an explicitly chosen local SQLite file. The website cannot upload files, write databases, fetch URLs, execute code, contact orbital catalogs or send commands to hardware.

## Boundaries

1. Python validates 1–8 uniquely named objects, 2–721 synchronized strictly ordered samples, a maximum two-hour horizon and finite bounded km/km/s vectors. The public catalog is smaller: three scenarios × three windows. Position components are bounded to 10 million km and velocities to 100 km/s as educational numerical limits, not universal physics constraints.
2. SGP4 uses a reviewed historical OMM at its original UTC epoch. Split Julian dates avoid adding small time offsets to a large floating-point day number. All propagator error codes fail the entire replay.
3. The nine-entry cache stores serialized reports, not mutable dictionaries. Each request receives a detached record. Content ID includes software version, source identity, models, units, histories and limitations; no wall-clock generation timestamp makes repeat runs unstable.
4. TypeScript owns only view state. Request generations and abort signals prevent stale results from replacing a later selection. Background tabs pause playback. Interpolation is bounded; no extrapolation. Changing scenarios disposes GPU buffers/materials/listeners/resize observers.
5. SQLite writes use parameterized statements and an immediate transaction. Duplicate IDs are idempotent. Update trigger refuses mutation. The database caps at 100 different runs, refuses new inserts at capacity, and never deletes records automatically. A person with filesystem write access can still alter the file: this is not tamper-proof storage.

## Decisions and trade-offs

- **Python rather than custom C++ propagation:** use a documented tested implementation, with compiled SGP4 acceleration when available and portable fallback. Reimplementing orbital mechanics would add risk without demonstrating better engineering.
- **TypeScript and Three.js:** strict domain contracts and small framework-free orchestration. WebGL is optional: XY projection, charts and numeric evidence remain useful without it. Bundled Three.js dominates client size (~141 kB gzip initially); no CDN improves offline availability and privacy. A future lazy renderer can reduce first-load bytes if measurements justify it.
- **SQL rather than a hosted database:** this is a local educational tool, not a multi-tenant service. No account data exists. Filesystem permissions and full-disk encryption are the user's responsibility.
- **Browser plus portable native bundle:** one maintained UI, served on loopback by Python or a frozen app. No administrator rights, installer service or auto-update. Platform-specific unsigned ZIP bundles do not imply mobile binary support.
- **Finite reviewed scenarios:** deliberately no generic input format or live orbital catalog. Extending science requires code review, independent reference fixtures, method documentation and tests. It is not an operational system with a switch to enable weapon features.

## Complexity

For N objects and S samples, pair screening is O(N²S) time, O(N²) event output; histories occupy O(NS) memory. Propagation and serialization are O(NS). The first run constructs bounded evidence; subsequent runs deserialize a finite cache entry. Display interpolation currently scans O(S) per object/cursor update; S ≤ 721 and N ≤ 3 in the catalog, keeping the implementation readable. Scene geometry is O(NS); markers update without rebuilding line geometry. Resource and request bounds are deliberate protections, not claims of unlimited scale.

## Failure handling

Unavailable local resources give generic HTTP errors. Invalid/duplicate/unbounded API options fail with 400; source/hidden paths with 404; foreign origins/Host with 403. A failed scenario keeps previous evidence visibly labeled and disables playback until a successful reload. Download links remain linked to that previous complete report, not a partially computed replacement. There is no claim of transactional atomicity across a separate export file and history database: CLI history can be committed even if writing the export later fails.
