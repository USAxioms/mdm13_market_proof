import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from wad18 import SCALE
from bounded_growth import (
    bounded_growth_step,
    verify_bound,
    verify_trajectory,
)


def test_zero_growth():
    result = bounded_growth_step(
        0,
        SCALE,
        10 * SCALE,
        SCALE,
    )

    assert result == 0


def test_growth_inside_capacity():
    x = 5 * SCALE
    capacity = 10 * SCALE

    result = bounded_growth_step(
        x,
        SCALE // 10,
        capacity,
        SCALE,
    )

    assert result > x


def test_capacity_boundary_is_fixed():
    capacity = 10 * SCALE

    result = bounded_growth_step(
        capacity,
        SCALE,
        capacity,
        SCALE,
    )

    assert result == capacity


def test_bound_check():
    capacity = 10 * SCALE

    assert verify_bound(5 * SCALE, capacity)
    assert not verify_bound(11 * SCALE, capacity)


def test_trajectory_check():
    capacity = 10 * SCALE

    states = [
        1 * SCALE,
        2 * SCALE,
        4 * SCALE,
        7 * SCALE,
    ]

    assert verify_trajectory(states, capacity)