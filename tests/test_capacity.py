import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from wad18 import SCALE
from capacity import (
    capacity_from_state,
    utilization,
    headroom,
    strain,
    capacity_violation,
    envelope_status,
)


def test_capacity():
    result = capacity_from_state(
        2 * SCALE,
        3 * SCALE,
    )

    assert result == 6 * SCALE


def test_utilization():
    result = utilization(
        5 * SCALE,
        10 * SCALE,
    )

    assert result == 5 * SCALE // 10


def test_headroom():
    result = headroom(
        3 * SCALE,
        10 * SCALE,
    )

    assert result == 7 * SCALE


def test_strain():
    result = strain(
        8 * SCALE,
        3 * SCALE,
    )

    assert result == 5 * SCALE


def test_no_violation():
    assert capacity_violation(
        5 * SCALE,
        10 * SCALE,
    ) == 0


def test_positive_violation():
    assert capacity_violation(
        12 * SCALE,
        10 * SCALE,
    ) == 2 * SCALE


def test_envelope_status():
    assert envelope_status(
        5 * SCALE,
        10 * SCALE,
    ) == "NORMAL"

    assert envelope_status(
        12 * SCALE,
        10 * SCALE,
    ) == "VIOLATION"