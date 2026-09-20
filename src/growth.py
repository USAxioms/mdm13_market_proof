"""
WAD-18 Growth Measurement
=========================

Normative path:
- signed arbitrary-precision integers
- WAD scale = 10^18
- no floating-point arithmetic
- deterministic
"""

from wad18 import (
    SCALE,
    add,
    sub,
    mul,
    div,
    abs_wad,
    square,
)


def growth_vector(current, previous):
    """Return exact WAD growth vector Δx = x_t - x_(t-1)."""
    if len(current) != len(previous):
        raise ValueError("Dimension mismatch")

    return [sub(a, b) for a, b in zip(current, previous)]


def squared_norm(vector):
    """Return Σ x_i² in WAD representation."""
    total = 0
    for value in vector:
        total = add(total, square(value))
    return total


def growth_magnitude(vector):
    """
    Deterministic WAD square-root certificate.

    Returns lower and upper WAD bounds for ||vector||.
    """
    value = squared_norm(vector)
    return sqrt_interval(value)


def sqrt_floor_wad(x):
    """
    Exact floor of sqrt(x) expressed in WAD.

    If x is WAD-scaled:
        x = X / SCALE

    then:
        sqrt(x) = sqrt(X*SCALE) / SCALE
    """
    if x < 0:
        raise ValueError("Square root of negative value")

    target = x * SCALE
    return integer_sqrt(target)


def sqrt_interval(x):
    """
    Return [lower, upper] WAD bounds containing sqrt(x).

    upper is the smallest integer whose square is >= target.
    """
    lower = sqrt_floor_wad(x)

    if lower * lower == x * SCALE:
        return lower, lower

    return lower, lower + 1


def growth_ratio(agent_growth, structural_growth, epsilon):
    """
    Exact WAD ratio:

        G_A / (G_S + epsilon)
    """
    denominator = add(structural_growth, epsilon)

    if denominator <= 0:
        raise ValueError("Invalid growth denominator")

    return div(agent_growth, denominator)


def growth_difference(agent_growth, structural_growth, coupling):
    """
    D_growth = G_A - λ G_S
    """
    return sub(
        agent_growth,
        mul(coupling, structural_growth),
    )


def classify_direction(previous, current):
    """
    Return integer direction for each component:

       +1 expansion
        0 unchanged
       -1 contraction
    """
    if len(previous) != len(current):
        raise ValueError("Dimension mismatch")

    result = []

    for old, new in zip(previous, current):
        if new > old:
            result.append(1)
        elif new < old:
            result.append(-1)
        else:
            result.append(0)

    return result


def integer_sqrt(n):
    """Exact integer square root: floor(sqrt(n))."""
    if n < 0:
        raise ValueError("Negative input")

    if n < 2:
        return n

    x = 1 << ((n.bit_length() + 1) // 2)

    while True:
        y = (x + n // x) // 2

        if y >= x:
            return x

        x = y
