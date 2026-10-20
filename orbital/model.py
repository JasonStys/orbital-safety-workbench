"""Immutable units/frame/sample contracts and bounded interpolation by Jason Stys.

Functions/classes: Sample, Track, validate_tracks, interpolate, closest_approaches.
Variables: Vec3 and supported sample/object limits. Exact lines: docs/CODE_INDEX.md.
"""

from dataclasses import asdict, dataclass
from math import isfinite, sqrt
from typing import Any

type Vec3 = tuple[float, float, float]


@dataclass(frozen=True)
class Sample:
    """A time offset in seconds, TEME-like position km, and velocity km/s."""

    t: float
    position: Vec3
    velocity: Vec3


@dataclass(frozen=True)
class Track:
    """One named history; provenance distinguishes historical propagation from fiction."""

    name: str
    kind: str
    samples: tuple[Sample, ...]


def validate_tracks(tracks: tuple[Track, ...]) -> None:
    """Require unique names and finite, strictly ordered, synchronized bounded samples."""
    if not 1 <= len(tracks) <= 8 or len({t.name for t in tracks}) != len(tracks):
        raise ValueError("Expected 1–8 uniquely named tracks")
    times = [s.t for s in tracks[0].samples]
    if not 2 <= len(times) <= 721 or times[0] != 0 or times[-1] > 7200:
        raise ValueError("Expected 2–721 samples covering at most two hours from zero")
    if any(b <= a for a, b in zip(times, times[1:], strict=False)):
        raise ValueError("Sample times must strictly increase")
    for track in tracks:
        if not track.name or len(track.name) > 80 or track.kind not in ("historical", "synthetic"):
            raise ValueError("Invalid track metadata")
        if [s.t for s in track.samples] != times:
            raise ValueError("Tracks must have identical time grids")
        for sample in track.samples:
            if (
                len(sample.position) != 3
                or len(sample.velocity) != 3
                or not all(isfinite(x) for x in (sample.t, *sample.position, *sample.velocity))
            ):
                raise ValueError("Samples must contain finite 3-vectors")
            if any(abs(x) > 10_000_000 for x in sample.position) or any(
                abs(x) > 100 for x in sample.velocity
            ):
                raise ValueError("Sample exceeds educational model bounds")


def interpolate(track: Track, time_s: float) -> Sample:
    """Return a bounded piecewise-linear display sample; never extrapolate."""
    if not isfinite(time_s) or not track.samples[0].t <= time_s <= track.samples[-1].t:
        raise ValueError("Time is outside track coverage")
    for left, right in zip(track.samples, track.samples[1:], strict=False):
        if time_s <= right.t:
            fraction = (time_s - left.t) / (right.t - left.t)
            p = tuple(
                a + fraction * (b - a) for a, b in zip(left.position, right.position, strict=True)
            )
            v = tuple(
                a + fraction * (b - a) for a, b in zip(left.velocity, right.velocity, strict=True)
            )
            return Sample(time_s, (p[0], p[1], p[2]), (v[0], v[1], v[2]))
    raise ValueError("No covered segment")  # defensive for callers bypassing validation


def closest_approaches(tracks: tuple[Track, ...]) -> list[dict[str, Any]]:
    """Find each pair's minimum over every linear segment, not animation samples.

    This is exact only for the sampled piecewise-linear histories. It is neither
    a nonlinear orbital event solver nor a probability or maneuver calculation.
    """
    validate_tracks(tracks)
    events: list[dict[str, Any]] = []
    for index, first in enumerate(tracks):
        for second in tracks[index + 1 :]:
            best = (float("inf"), 0.0)
            for n in range(len(first.samples) - 1):
                a, b = first.samples[n], first.samples[n + 1]
                c, d = second.samples[n], second.samples[n + 1]
                r = tuple(x - y for x, y in zip(a.position, c.position, strict=True))
                delta = tuple(
                    (y - x) - (v - u)
                    for x, y, u, v in zip(
                        a.position, b.position, c.position, d.position, strict=True
                    )
                )
                norm2 = sum(x * x for x in delta)
                fraction = (
                    max(0.0, min(1.0, -sum(x * y for x, y in zip(r, delta, strict=True)) / norm2))
                    if norm2
                    else 0.0
                )
                distance = sqrt(sum((x + fraction * y) ** 2 for x, y in zip(r, delta, strict=True)))
                candidate = (distance, a.t + fraction * (b.t - a.t))
                best = min(best, candidate)
            events.append(
                {
                    "first": first.name,
                    "second": second.name,
                    "distance_km": best[0],
                    "time_s": best[1],
                    "collision_probability": None,
                    "assessment": "Insufficient information: covariance and physical size are absent",
                    "method": "continuous minimum of sampled piecewise-linear histories",
                }
            )
    return events


def track_record(track: Track) -> dict[str, Any]:
    """Serialize an immutable track; callers cannot mutate cached dataclasses."""
    return asdict(track)
