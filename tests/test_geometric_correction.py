import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from wad18 import SCALE
from geometric_correction import (
    correction_error,
    correction_factor,
    correction_amount,
    corrected_state,
    correction_required,
    verify_correction,
)


def test_correction_error():
    result = correction_error(
        12 * SCALE,
        10 * SCALE,
    )

    assert result == 2 * SCALE


def test_correction_factor():
    result = correction_factor(
        12 * SCALE // 10,
    )

    assert result == 2 * SCALE // 10


def test_no_correction_inside_capacity():
    result = correction_amount(
        5 * SCALE,
        10 * SCALE,
        SCALE // 2,
    )

    assert result == 0


def test_correction_above_capacity():
    result = correction_amount(
        12 * SCALE,
        10 * SCALE,
        SCALE // 2,
    )

    assert result == SCALE


def test_corrected_state():
    result = corrected_state(
        12 * SCALE,
        10 * SCALE,
        SCALE // 2,
    )

    assert result == 11 * SCALE


def test_correction_required():
    assert not correction_required(
        8 * SCALE,
        10 * SCALE,
    )

    assert correction_required(
        12 * SCALE,
        10 * SCALE,
    )


def test_correction_verification():
    corrected = corrected_state(
        12 * SCALE,
        10 * SCALE,
        SCALE,
    )

    assert verify_correction(
        12 * SCALE,
        10 * SCALE,
        corrected,
    )