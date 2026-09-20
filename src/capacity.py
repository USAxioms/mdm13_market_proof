"""
WAD-18 Capacity Envelope
========================
"""

from wad18 import SCALE, add, sub, mul, div


def capacity_from_state(reference_state, multiplier):
    """
    K = reference_state * multiplier
    """
    if reference_state < 0:
        raise ValueError("Reference state must be non-negative")

    if multiplier <= 0:
        raise ValueError("Multiplier must be positive")

    return mul(reference_state, multiplier)


def utilization(state, capacity):
    """Return WAD utilization state/capacity."""
    if capacity <= 0:
        raise ValueError("Capacity must be positive")

    if state < 0:
        raise ValueError("State must be non-negative")

    return div(state, capacity)


def headroom(state, capacity):
    """Return remaining capacity as a WAD value."""
    if capacity < 0:
        raise ValueError("Capacity must be non-negative")

    return sub(capacity, state)


def strain(agent_state, structural_state):
    """
    Difference between normalized subsystem utilization.
    """
    return sub(agent_state, structural_state)


def capacity_violation(state, capacity):
    """
    Return deterministic violation magnitude.

    0 means no violation.
    """
    if state < 0:
        return -state

    if state > capacity:
        return state - capacity

    return 0


def envelope_status(state, capacity):
    """
    NORMAL if inside envelope.
    VIOLATION otherwise.
    """
    return "NORMAL" if capacity_violation(state, capacity) == 0 else "VIOLATION"