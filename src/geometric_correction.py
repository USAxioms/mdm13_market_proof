"""
WAD-18 Geometric Correction
===========================

Correction operator for states approaching or exceeding
a declared capacity envelope.

This module does not assert a physical market crash.
"""

from wad18 import SCALE, sub, mul


def correction_error(state, capacity):
    """
    Signed distance from the capacity boundary.

    Positive = above capacity.
    Negative = below capacity.
    """
    return sub(state, capacity)


def correction_factor(utilization):
    """
    Linear correction factor:

        c = utilization - 1

    Positive values indicate boundary excess.
    """
    return sub(utilization, SCALE)


def correction_amount(state, capacity, gain):
    """
    Deterministic correction magnitude.

    correction = gain * max(state - capacity, 0)
    """
    excess = correction_error(state, capacity)

    if excess <= 0:
        return 0

    return mul(gain, excess)


def corrected_state(state, capacity, gain):
    """
    Apply deterministic boundary correction.

    If state is inside the envelope, state is unchanged.
    """
    amount = correction_amount(
        state,
        capacity,
        gain,
    )

    corrected = state - amount

    if corrected < 0:
        return 0

    return corrected


def correction_required(state, capacity):
    return state > capacity


def verify_correction(state, capacity, corrected):
    """
    Correction is valid if:
    - corrected >= 0
    - corrected <= capacity
    - corrected <= original state
    """
    if corrected < 0:
        return False

    if corrected > capacity:
        return False

    if corrected > state:
        return False

    return True