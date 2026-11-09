"""Illustrative distance-threshold windows by Jason Stys.

Function: screening_windows. Variables: relative segment vectors, closest-line fraction and roots.
No covariance, collision probability or maneuver guidance. Exact lines: docs/CODE_INDEX.md.
"""

import math
from typing import Any

from orbital.model import Track, validate_tracks


def screening_windows(tracks: tuple[Track, ...], radius_km: float) -> list[dict[str, Any]]:
    """Solve closed distance <= radius windows for the sampled piecewise-linear histories.

    Fixed distances are illustrative display thresholds, not safety radii. Stationary relative
    segments, zero-duration tangencies and window-edge censoring stay explicit. Touching windows
    merge within 1e-9 seconds solely to absorb floating-point endpoint roundoff.
    """
    validate_tracks(tracks)
    if (
        type(radius_km) not in (int, float)
        or not math.isfinite(radius_km)
        or not 0 < radius_km <= 1000
    ):
        raise ValueError("Expected illustrative radius in (0,1000] km")
    result = []
    for index, first in enumerate(tracks):
        for second in tracks[index + 1 :]:
            windows: list[dict[str, Any]] = []
            for n in range(len(first.samples) - 1):
                a, b = first.samples[n : n + 2]
                c, d = second.samples[n : n + 2]
                relative = [x - y for x, y in zip(a.position, c.position, strict=True)]
                delta = [
                    (y - x) - (v - u)
                    for x, y, u, v in zip(
                        a.position, b.position, c.position, d.position, strict=True
                    )
                ]
                speed2 = sum(x * x for x in delta)
                if speed2 == 0:
                    if sum(x * x for x in relative) > radius_km**2:
                        continue
                    entry, exit_ = 0.0, 1.0
                else:
                    center = -sum(x * y for x, y in zip(relative, delta, strict=True)) / speed2
                    perpendicular2 = sum(
                        (x + center * y) ** 2 for x, y in zip(relative, delta, strict=True)
                    )
                    if perpendicular2 > radius_km**2:
                        continue
                    half = math.sqrt(max(0, (radius_km**2 - perpendicular2) / speed2))
                    entry, exit_ = max(0.0, center - half), min(1.0, center + half)
                    if entry > exit_:
                        continue
                start = a.t + entry * (b.t - a.t)
                end = a.t + exit_ * (b.t - a.t)
                if windows and start <= windows[-1]["end_s"] + 1e-9:
                    windows[-1]["end_s"] = max(end, windows[-1]["end_s"])
                else:
                    windows.append({"start_s": start, "end_s": end})
            for window in windows:
                window.update(
                    duration_s=window["end_s"] - window["start_s"],
                    start_censored=window["start_s"] == 0,
                    end_censored=window["end_s"] == first.samples[-1].t,
                )
            result.append(
                {
                    "first": first.name,
                    "second": second.name,
                    "threshold_km": radius_km,
                    "windows": windows,
                    "total_duration_s": sum(w["duration_s"] for w in windows),
                }
            )
    return result
