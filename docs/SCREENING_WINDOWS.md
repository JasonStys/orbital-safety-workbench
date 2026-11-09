# Inspect illustrative distance windows

Expand distance-threshold windows beneath closest approaches. The workbench solves entry/exit intervals for **closed** distances at or below1,5 or10km using each sampled piecewise-linear relative path. It preserves stationary-inside intervals, zero-duration tangencies, no-window pairs and start/end censoring. Adjacent windows merge within1e-9s to absorb floating-point endpoint roundoff. A button moves replay to the nearest whole second; exact fractional boundaries stay in the ledger.

Thresholds are illustrative teaching values, not safety radii. The calculations are exact only for the represented linear segments at floating-point precision, not continuous nonlinear orbital dynamics. Covariance, object sizes and authenticated current tracking are absent. No collision probability, maneuver advice, targeting or interception is added. The single archived ISS trace has no pairwise windows and remains replayed only at its historical epoch.

JSON/HTML exports and immutable CLI history preserve the windows under the evidence hash. The existing unit-labeled CSV remains the original sampled histories. Analytic tests independently cover between-sample crossings, tangencies, stationary/retreating pairs, merged boundaries and invalid radii.
