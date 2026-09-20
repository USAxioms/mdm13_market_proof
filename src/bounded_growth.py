"""
WAD-18 Bounded Growth Dynamics
==============================

Discrete bounded-growth operator.

The normative state is an integer WAD value.
"""

from wad18 import SCALE, add, sub, mul, div


def bounded_growth_step(x, rate, capacity, dt):
    """
    Logistic-style bounded growth:

        x_next =
            x + dt * rate * x * (1 - x/capacity)

    All quantities are WAD integers.
    """
    if capacity <= 0:
        raise ValueError("Capacity must be positive")

    if x < 0:
        raise ValueError("State must be non-negative")

    utilization = div(x, capacity)

    remaining = sub(SCALE, utilization)

    growth_term = mul(
        mul(rate, x),
        remaining,
    )

    return add(
        x,
        mul(dt, growth_term),
    )


def bounded_interval_step(x, rate, capacity, dt):
    """
    Apply bounded step and return the candidate state.

    The invariant checker is separate so the mathematics
    cannot silently hide an invalid trajectory.
    """
    return bounded_growth_step(
        x,
        rate,
        capacity,
        dt,
    )


def verify_bound(x, capacity):
    """Return True iff 0 <= x <= capacity."""
    return 0 <= x <= capacity


def verify_trajectory(states, capacity):
    """Verify every state remains inside the declared envelope."""
    return all(
        verify_bound(state, capacity)
        for state in states
    )