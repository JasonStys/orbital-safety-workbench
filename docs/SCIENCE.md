# Scientific method, provenance and limits

## Historical replay

`iss-2024.json` reproduces the public ISS OMM example from [Skyfield's satellite documentation](https://rhodesmill.org/skyfield/earth-satellites.html), epoch **2024-05-06 19:53:04.999776 UTC**. No current orbital catalog is fetched. Source SHA-256 hashes the repository's UTF-8 fixture bytes, including formatting; it identifies this copy, not the upstream web page or satellite's physical state.

The [python-sgp4 implementation](https://pypi.org/project/sgp4/) initializes that OMM with SGP4/WGS72. Samples are evaluated every 10 seconds for 30, 60 or 120 minutes starting at the fixture epoch. Values are returned in **TEME** Cartesian coordinates: position km, velocity km/s. The Earth display is a WGS72-radius reference sphere (6378.135 km), not a textured geodetic map. There is no Earth-fixed conversion or longitude/latitude/ground-track claim. Radial height is Euclidean radius minus this reference radius, **not geodetic altitude**.

SGP4 evaluates a mean-element model, not osculating Kepler elements. Old mean elements should not be treated as current predictions. See [CelesTrak GP formats](https://celestrak.org/NORAD/documentation/gp-data-formats.php) for format context.

## Synthetic cases

The synthetic traces are mathematical, inertial-like Cartesian histories with a shared circular XY projection and independently prescribed Z offsets. Their velocities are analytic derivatives of those prescriptions at sample times. They are **not gravitationally integrated orbital solutions** and are not real satellites or debris. Display interpolation linearly interpolates positions and sampled velocities independently; the latter is not exactly the derivative of a position chord.

Demo A/B have a fictional crossing at 907 seconds in the crossing scenario. It deliberately lies between 900 and 910 second samples. The separated case adds large constant Z offsets. Demo C exercises all three object pairs and endpoint minima.

## Closest-approach screening

Each segment's relative position is affine in the segment fraction. The squared distance is minimized on that closed segment; zero relative displacement returns the segment's first timestamp. Each pair's minimum over every segment is retained, with earliest timestamp breaking exact ties. This finds the **continuous minimum of sampled piecewise-linear histories**, not just the smallest discrete sample.

That distinction matters: it does not refine the underlying nonlinear SGP4 model, solve an orbital encounter, assess collision risk or propose actions. No covariance matrices or object radii are provided; every collision-probability field is JSON `null`, never zero. [NASA CARA](https://www.nasa.gov/cara/step-2-close-approach-risk-assessment/) describes why proximity alone is insufficient for risk assessment.

## Verification, not certification

- A fixed Vanguard-1 epoch vector from the published [Vallado verification output](https://github.com/brandon-rhodes/python-sgp4/blob/master/sgp4/tcppver.out) is checked with absolute tolerances 1e-7 km position / 1e-9 km/s velocity. The fixture input is the associated historical verification TLE, not a current catalog entry.
- Native and pure-Python OMM implementations are compared at multiple offsets/windows. They implement the same algorithm; this is a portability check, not independent model validation.
- Analytic relative-motion fixtures, bounded property tests, endpoints, ties and swapped object order test screening logic.

Numerical agreement does **not** establish real-world orbit accuracy, an uncertainty bound, mission suitability, safety certification or compliance. No operational guarantees or performance qualifications are made.
