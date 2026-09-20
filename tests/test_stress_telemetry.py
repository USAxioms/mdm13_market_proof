import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from wad18 import SCALE
from growth_correlation import (
    correlation_interval,
    rolling_growth_correlation,
    threshold_state,
)


def test_perfect_positive_correlation():
    x = [1, 2, 3, 4]
    y = [2, 4, 6, 8]

    low, high, status = correlation_interval(x, y)

    assert status == "CERTIFIED"
    assert low == SCALE
    assert high == SCALE


def test_perfect_negative_correlation():
    x = [1, 2, 3, 4]
    y = [8, 6, 4, 2]

    low, high, status = correlation_interval(x, y)

    assert status == "CERTIFIED"
    assert low == -SCALE
    assert high == -SCALE


def test_zero_variance():
    x = [1, 1, 1]
    y = [1, 2, 3]

    low, high, status = correlation_interval(x, y)

    assert status == "UNDEFINED_ZERO_VARIANCE"


def test_rolling_window():
    x = [1, 2, 3, 4]
    y = [2, 4, 6, 8]

    records = rolling_growth_correlation(x, y, 3)

    assert len(records) == 2
    assert records[0]["rho_low"] == SCALE
    assert records[1]["rho_high"] == SCALE


def test_threshold_classification():
    assert (
        threshold_state(
            -SCALE,
            -SCALE,
            -SCALE // 2,
            0,
        )
        == "COLLAPSED"
    )