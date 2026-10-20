"""Numerical/reference/property regression tests by Jason Stys.

Functions: fixture track, test_* assertions. Variables: published Vanguard reference vectors.
Exact function/variable line map: docs/CODE_INDEX.md. No live space-object API is used.
"""

import json
from dataclasses import replace
from importlib.resources import files
from math import isfinite

import pytest
from hypothesis import given
from hypothesis import strategies as st
from sgp4 import omm
from sgp4.api import Satrec
from sgp4.model import Satrec as PythonSatrec

from orbital.model import Sample, Track, closest_approaches, interpolate, validate_tracks
from orbital.scenarios import build_run, catalog, propagate_iss, run_id, synthetic_tracks

TLE = (
    "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753",
    "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667",
)
# Published Vallado verification output, NOT computed by the code under test.
# https://github.com/brandon-rhodes/python-sgp4/blob/master/sgp4/tcppver.out lines 1–2.
REFERENCE_POSITION = (7022.46529266, -1400.08296755, 0.03995155)
REFERENCE_VELOCITY = (1.893841015, 6.405893759, 4.534807250)


def track(name="A", start=(0.0, 0.0, 0.0), end=(10.0, 0.0, 0.0)):
    """Build a minimal valid two-sample history with stationary display velocities."""
    return Track(name, "synthetic", (Sample(0, start, (0, 0, 0)), Sample(10, end, (0, 0, 0))))


def test_published_sgp4_vectors():
    """Validate imported propagation against rounded published values, not physical truth."""
    satellite = Satrec.twoline2rv(*TLE)
    error, position, velocity = satellite.sgp4(satellite.jdsatepoch, satellite.jdsatepochF)
    assert error == 0
    assert position == pytest.approx(REFERENCE_POSITION, abs=1e-7)
    assert velocity == pytest.approx(REFERENCE_VELOCITY, abs=1e-9)


@pytest.mark.parametrize("minutes", [30, 60, 120])
def test_omm_native_python_portability(minutes):
    """Compare two implementations of the same algorithm at reviewed ISS timestamps."""
    fields = json.loads(files("orbital").joinpath("resources/iss-2024.json").read_bytes())
    native, pure = Satrec(), PythonSatrec()
    omm.initialize(native, fields)
    omm.initialize(pure, fields)
    for offset in (0, minutes / 2, minutes):
        expected = native.sgp4(native.jdsatepoch, native.jdsatepochF + offset / 1440)
        actual = pure.sgp4(pure.jdsatepoch, pure.jdsatepochF + offset / 1440)
        assert actual[0] == expected[0] == 0
        assert actual[1] == pytest.approx(expected[1], abs=1e-7)
        assert actual[2] == pytest.approx(expected[2], abs=1e-9)


@pytest.mark.parametrize("scenario", [item["id"] for item in catalog()])
@pytest.mark.parametrize("minutes", [30, 60, 120])
def test_run_contract(scenario, minutes):
    """Every supported combination has finite bounded samples, explicit frame and reproducible ID."""
    run = build_run(scenario, minutes)
    assert run_id(run) == run["id"]
    assert run["provenance"]["real_time"] is False
    assert "2024-05-06" in run["provenance"]["epoch_utc"]
    assert run["units"] == {"position": "km", "velocity": "km/s", "time": "s"}
    for item in run["tracks"]:
        assert len(item["samples"]) == minutes * 6 + 1
        assert item["samples"][-1]["t"] == minutes * 60
        assert all(isfinite(x) for sample in item["samples"] for x in sample["position"])
    assert all(event["collision_probability"] is None for event in run["events"])
    run["limitations"].clear()
    assert build_run(scenario, minutes)["limitations"]  # cache cannot leak mutable objects


@pytest.mark.parametrize(
    "scenario,minutes", [("unknown", 60), ("iss-archive", 0), ("iss-archive", 121)]
)
def test_reject_unsupported_run(scenario, minutes):
    """Finite input catalog prevents unbounded propagation/cache growth."""
    with pytest.raises(ValueError):
        build_run(scenario, minutes)


def test_invalid_direct_generators():
    """Even internal helpers enforce finite reviewed windows."""
    with pytest.raises(ValueError):
        propagate_iss(-1)
    with pytest.raises(ValueError):
        synthetic_tracks(500, False)
    changed = catalog()
    changed[0]["id"] = "bad"
    assert catalog()[0]["id"] == "iss-archive"


def test_between_sample_minimum():
    """An event between timestamps is found, not missed by discrete-only screening."""
    a = track()
    b = track("B", (7, 1, 0), (7, 1, 0))
    event = closest_approaches((a, b))[0]
    assert event["time_s"] == pytest.approx(7)
    assert event["distance_km"] == pytest.approx(1)
    assert event["collision_probability"] is None
    assert closest_approaches((a,)) == []


@pytest.mark.parametrize("position,time", [((-4, 1, 0), 0), ((40, 1, 0), 10)])
def test_endpoint_minima(position, time):
    """The clamped relative-motion minimum includes both segment endpoints."""
    event = closest_approaches((track(), track("B", position, position)))[0]
    assert event["time_s"] == time


def test_constant_relative_motion():
    """Equal velocities produce no division by zero and deterministic earliest tie."""
    assert closest_approaches((track(), track("B", (0, 2, 0), (10, 2, 0))))[0]["time_s"] == 0


@given(st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False))
def test_pair_symmetry(y):
    """Bounded arbitrary offsets preserve distance and event time when pair order swaps."""
    a, b = track(), track("B", (7, y, 0), (7, y, 0))
    left, right = closest_approaches((a, b))[0], closest_approaches((b, a))[0]
    assert left["distance_km"] == pytest.approx(right["distance_km"])
    assert left["time_s"] == pytest.approx(right["time_s"])
    assert left["distance_km"] >= 0


@pytest.mark.parametrize("time", [0, 3, 10])
def test_interpolation(time):
    """The display interpolation matches linear analytic positions including endpoints."""
    assert interpolate(track(), time).position == pytest.approx((time, 0, 0))


@pytest.mark.parametrize("time", [-1, 11, float("nan"), float("inf")])
def test_interpolation_bounds(time):
    """No extrapolation or NaN display offsets are accepted."""
    with pytest.raises(ValueError):
        interpolate(track(), time)


def test_single_sample_interpolation():
    """Defensive path rejects a caller bypassing the valid-history contract."""
    with pytest.raises(ValueError, match="No covered"):
        interpolate(replace(track(), samples=(track().samples[0],)), 0)


@pytest.mark.parametrize(
    "tracks",
    [
        (),
        (track(), track()),
        (replace(track(), name=""),),
        (replace(track(), kind="live"),),
        (replace(track(), samples=()),),
        (replace(track(), samples=(Sample(1, (0, 0, 0), (0, 0, 0)),) * 2),),
        (replace(track(), samples=(track().samples[0], Sample(8000, (0, 0, 0), (0, 0, 0)))),),
        (replace(track(), samples=(track().samples[0], Sample(0, (0, 0, 0), (0, 0, 0)))),),
        (
            track(),
            replace(track("B"), samples=(track().samples[0], Sample(9, (0, 0, 0), (0, 0, 0)))),
        ),
        (
            replace(
                track(), samples=(track().samples[0], Sample(10, (float("nan"), 0, 0), (0, 0, 0)))
            ),
        ),
        (replace(track(), samples=(track().samples[0], Sample(10, (1e8, 0, 0), (0, 0, 0)))),),
    ],
)
def test_invalid_histories(tracks):
    """Malformed metadata, time grids and extreme/nonfinite samples fail closed."""
    with pytest.raises(ValueError):
        validate_tracks(tracks)


def test_synthetic_screening_is_not_operational():
    """The fictional crossing is explicit and the separated baseline remains distinct."""
    crossing = build_run("synthetic-crossing")["events"][0]
    assert crossing["time_s"] == 907
    assert crossing["distance_km"] < 1e-12
    assert build_run("synthetic-separated")["events"][0]["distance_km"] > 200


def test_sgp4_failure_is_not_partial(monkeypatch):
    """A propagator error rejects the complete result rather than emit misleading samples."""

    class BrokenSat:
        """Minimal failed dependency double; omm initialization is independently replaced."""

        def sgp4(self, *args):
            """Report an SGP4 numerical error with no usable position or velocity."""
            return 6, (), ()

    monkeypatch.setattr("orbital.scenarios.Satrec", BrokenSat)
    monkeypatch.setattr("orbital.scenarios.omm.initialize", lambda *_: None)
    with pytest.raises(ValueError, match="SGP4 failed"):
        propagate_iss(30)
