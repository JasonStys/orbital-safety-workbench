# Data and third-party notices

- Historical ISS OMM: numerical public scientific example at [Skyfield satellite docs](https://rhodesmill.org/skyfield/earth-satellites.html), epoch 2024-05-06. Stored locally, never fetched at runtime. Source byte hash included in reports. Upstream prose is not copied.
- SGP4: [python-sgp4](https://github.com/brandon-rhodes/python-sgp4), MIT-licensed, packaged runtime dependency. Native implementation uses the published Vallado algorithm; Python portability code follows the same model. Its upstream license is distributed with package metadata in native bundles.
- Verification vector: first Vanguard-1 record from published `tcppver.out` in that upstream project, associated `SGP4-VER.TLE`. Numerical values used solely for verification.
- [Three.js](https://github.com/mrdoob/three.js), MIT-licensed, bundled locally. No textures or remote imagery. Preserve its distributed license notice in source dependencies/builds.
- TypeScript, Vite, Vitest, Playwright, axe, PyInstaller and Python tooling are development/build dependencies, not independent safety certifications. Full resolved versions/hashes/integrity are in `package-lock.json`, `requirements.lock` and `requirements-dev.lock`. Consult each package's own distributed license.

All synthetic cases are authored for this project and do not represent any real object, operator or mission. Jason Stys authorship applies to this application's implementation, not ownership of upstream libraries, scientific algorithms or public data.
