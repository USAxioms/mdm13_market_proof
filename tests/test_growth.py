import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from wad18 import SCALE
from growth import (
    growth_vector,
    squared_norm,
    growth_magnitude,
    growth_ratio,
    growth_difference,
)


def test_growth_vector():
    previous = [SCALE, 2 * SCALE]
    current = [2 * SCALE, SCALE]

    result = growth_vector(current, previous)

    assert result == [SCALE, -SCALE]


def test_squared_norm():
    vector = [SCALE, SCALE]

    assert squared_norm(vector) == 2 * SCALE


def test_growth_magnitude_interval():
    vector = [SCALE, 0]

    low, high = growth_magnitude(vector)

    assert low == SCALE
    assert high == SCALE


def test_growth_ratio():
    agent = 2 * SCALE
    structural = SCALE
    epsilon = SCALE // 1000

    ratio = growth_ratio(agent, structural, epsilon)

    assert ratio > SCALE


def test_growth_difference():
    agent = 3 * SCALE
    structural = SCALE
    coupling = 2 * SCALE

    result = growth_difference(agent, structural, coupling)

    assert result == SCALE