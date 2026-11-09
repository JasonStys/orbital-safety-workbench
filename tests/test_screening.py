"""Independent linear distance-window geometry by Jason Stys.

Functions: track and test_*; variables: analytic crossings, tangencies and stationary histories.
Thresholds are illustrative, never operational safety radii. Exact lines: docs/CODE_INDEX.md.
"""

import math

import pytest

from orbital.model import Sample, Track
from orbital.scenarios import build_run
from orbital.screening import screening_windows


def track(name: str, positions: list[tuple[float, float, float]]) -> Track:
    """Use ten-second samples with no implied physical orbital velocities."""
    return Track(
        name, "synthetic", tuple(Sample(i * 10, p, (0, 0, 0)) for i, p in enumerate(positions))
    )


def test_analytic_between_sample_crossing_and_tangency():
    """x travels -10..10 over10s, so radius2 gives [4,6]; y=2 instead touches at5 only."""
    fixed = track("fixed", [(0, 0, 0), (0, 0, 0)])
    crossing = track("moving", [(-10, 0, 0), (10, 0, 0)])
    row = screening_windows((fixed, crossing), 2)[0]
    assert row["windows"] == [
        {"start_s": 4, "end_s": 6, "duration_s": 2, "start_censored": False, "end_censored": False}
    ]
    tangent = track("tangent", [(-10, 2, 0), (10, 2, 0)])
    assert screening_windows((fixed, tangent), 2)[0]["windows"][0]["duration_s"] == 0
    absent = track("absent", [(-10, 3, 0), (10, 3, 0)])
    assert screening_windows((fixed, absent), 2)[0]["windows"] == []


def test_stationary_merged_edges_and_missed_segment():
    """Stationary-inside spans merge across samples and window boundaries stay censored."""
    fixed = track("fixed", [(0, 0, 0)] * 3)
    inside = track("inside", [(1, 0, 0)] * 3)
    window = screening_windows((fixed, inside), 2)[0]["windows"][0]
    assert window["start_s"] == 0 and window["end_s"] == 20
    assert window["start_censored"] and window["end_censored"]
    outside = track("outside", [(3, 0, 0)] * 3)
    assert screening_windows((fixed, outside), 2)[0]["total_duration_s"] == 0
    retreat = track("retreat", [(10, 0, 0), (20, 0, 0), (30, 0, 0)])
    assert screening_windows((fixed, retreat), 2)[0]["windows"] == []
    assert screening_windows((fixed,), 2) == []


@pytest.mark.parametrize("radius", [0, -1, math.nan, math.inf, True, 1001])
def test_invalid_threshold(radius):
    """Invalid radii cannot produce plausible-looking screening results."""
    with pytest.raises(ValueError):
        screening_windows((track("a", [(0, 0, 0)] * 2),), radius)


def test_run_includes_all_illustrative_thresholds_without_probability():
    """Three synthetic objects produce three pairs at three thresholds; the single archive has none."""
    run = build_run("synthetic-crossing", 30)
    assert len(run["screening_windows"]) == 9
    assert all(event["collision_probability"] is None for event in run["events"])
    assert build_run("iss-archive", 30)["screening_windows"] == []
