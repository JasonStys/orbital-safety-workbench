"""Reviewed civilian fixtures and bounded scientific runs by Jason Stys.

Functions: catalog, propagate_iss, synthetic_tracks, build_run, run_id.
Variables: CATALOG, WINDOWS, EARTH_RADIUS_KM, LIMITATIONS; line index in docs/CODE_INDEX.md.
"""

import hashlib
import json
from datetime import UTC, datetime, timedelta
from functools import lru_cache
from importlib.resources import files
from math import cos, pi, sin
from typing import Any

from sgp4 import omm
from sgp4.api import SGP4_ERRORS, Satrec, jday

from orbital import VERSION
from orbital.model import Sample, Track, closest_approaches, track_record, validate_tracks

EARTH_RADIUS_KM = 6378.135
WINDOWS = (30, 60, 120)
CATALOG = (
    {
        "id": "iss-archive",
        "title": "ISS · archived orbit",
        "kind": "historical",
        "summary": "Replay public ISS mean elements at their May 2024 epoch, not today's sky.",
    },
    {
        "id": "synthetic-crossing",
        "title": "Crossing histories · synthetic",
        "kind": "synthetic",
        "summary": "Three fictional traces demonstrate continuous between-sample screening.",
    },
    {
        "id": "synthetic-separated",
        "title": "Separated histories · synthetic",
        "kind": "synthetic",
        "summary": "Three fictional traces with large spatial offsets; a comparison baseline.",
    },
)
LIMITATIONS = (
    "Educational replay, not navigation, operational collision assessment or flight software.",
    "No covariance or physical object sizes: collision probability cannot be calculated.",
    "SGP4 numerical agreement does not establish physical accuracy of historical elements.",
    "Screening is exact only for the sampled piecewise-linear histories, not nonlinear motion.",
    "Radial height above a WGS72 reference sphere is not geodetic altitude. No ground track.",
    "No intercept, targeting, fragmentation, propulsion or maneuver recommendations.",
)


def catalog() -> list[dict[str, str]]:
    """Return detached public descriptors so callers cannot mutate the reviewed catalog."""
    return [dict(item) for item in CATALOG]


def propagate_iss(minutes: int) -> tuple[Track, dict[str, Any]]:
    """Propagate reviewed OMM only from its own UTC epoch; return TEME km and km/s.

    minutes is a reviewed horizon. jday preserves split-date precision, and any
    SGP4 error fails the complete run rather than displaying partial trajectories.
    """
    if minutes not in WINDOWS:
        raise ValueError("Unsupported horizon")
    raw = files("orbital").joinpath("resources/iss-2024.json").read_bytes()
    fields = json.loads(raw)
    satellite = Satrec()
    omm.initialize(satellite, fields)
    epoch = datetime.fromisoformat(fields["EPOCH"]).replace(tzinfo=UTC)
    samples = []
    for seconds in range(0, minutes * 60 + 1, 10):
        date = epoch + timedelta(seconds=seconds)
        jd, fraction = jday(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second + date.microsecond / 1_000_000,
        )
        error, position, velocity = satellite.sgp4(jd, fraction)
        if error:
            raise ValueError(f"SGP4 failed: {SGP4_ERRORS.get(error, 'unknown error')}")
        samples.append(Sample(float(seconds), tuple(position), tuple(velocity)))
    provenance = {
        "epoch_utc": epoch.isoformat(),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "source": "https://rhodesmill.org/skyfield/earth-satellites.html",
        "source_description": "Public ISS OMM example, historical epoch 2024-05-06",
        "model": "SGP4 2.27 / WGS72",
        "frame": "TEME",
        "real_time": False,
    }
    return Track("ISS (ZARYA)", "historical", tuple(samples)), provenance


def synthetic_tracks(minutes: int, separated: bool) -> tuple[Track, ...]:
    """Create deterministic fictional histories, NOT physical or maneuver simulations.

    The two main traces exchange phase near 907 seconds. Discrete samples alone
    miss the exact piecewise-linear minimum; a third trace tests multi-pair handling.
    """
    if minutes not in WINDOWS:
        raise ValueError("Unsupported horizon")
    tracks = []
    for index, name in enumerate(("Demo A", "Demo B", "Demo C")):
        samples = []
        for seconds in range(0, minutes * 60 + 1, 10):
            angle = seconds * 2 * pi / 5600
            offset = (seconds - 907) * 0.008
            z = 0.0 if index == 0 else (offset if index == 1 else 160.0)
            z += 250.0 * index if separated else 0.0
            position = (6900 * cos(angle), 6900 * sin(angle), z)
            velocity = (
                -6900 * 2 * pi / 5600 * sin(angle),
                6900 * 2 * pi / 5600 * cos(angle),
                0.008 if index == 1 else 0.0,
            )
            samples.append(Sample(float(seconds), position, velocity))
        tracks.append(Track(name, "synthetic", tuple(samples)))
    return tuple(tracks)


def run_id(run: dict[str, Any]) -> str:
    """Hash canonical JSON excluding the identifier; deterministic provenance, not a signature."""
    content = {key: value for key, value in run.items() if key != "id"}
    return hashlib.sha256(
        json.dumps(content, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


@lru_cache(maxsize=9)
def _run_json(scenario: str, minutes: int) -> str:
    """Cache serialized finite reviewed inputs, never mutable report objects."""
    if scenario not in {item["id"] for item in CATALOG} or minutes not in WINDOWS:
        raise ValueError("Unknown scenario or unsupported horizon")
    tracks: tuple[Track, ...]
    if scenario == "iss-archive":
        track, provenance = propagate_iss(minutes)
        tracks = (track,)
    else:
        tracks = synthetic_tracks(minutes, scenario == "synthetic-separated")
        provenance = {
            "epoch_utc": "2024-05-06T00:00:00+00:00",
            "source": "built-in synthetic",
            "source_description": "Deterministic fictional traces, no real objects",
            "source_sha256": hashlib.sha256(b"synthetic-traces-v1").hexdigest(),
            "model": "Fictional sampled histories v1",
            "frame": "synthetic Cartesian",
            "real_time": False,
        }
    validate_tracks(tracks)
    result: dict[str, Any] = {
        "schema_version": 1,
        "software_version": VERSION,
        "author": "Jason Stys",
        "scenario": scenario,
        "horizon_minutes": minutes,
        "sample_interval_s": 10,
        "units": {"position": "km", "velocity": "km/s", "time": "s"},
        "earth_radius_km": EARTH_RADIUS_KM,
        "provenance": provenance,
        "tracks": [track_record(track) for track in tracks],
        "events": closest_approaches(tracks),
        "limitations": list(LIMITATIONS),
    }
    result["id"] = run_id(result)
    return json.dumps(result, allow_nan=False, sort_keys=True)


def build_run(scenario: str, minutes: int = 60) -> dict[str, Any]:
    """Return a detached reproducible report for one of nine bounded input combinations."""
    return dict(json.loads(_run_json(scenario, minutes)))
