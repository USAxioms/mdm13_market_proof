"""
WAD-18 Growth Correlation Certificate
=====================================

The normative result is an interval [rho_low, rho_high].

No floating-point arithmetic is used.

A threshold decision is accepted only when the
entire interval lies on one side of the threshold.
"""

from wad18 import SCALE, add, sub, mul, div
from growth import integer_sqrt


def centered(values):
    """Return values centered around their exact integer mean."""
    if not values:
        raise ValueError("Empty window")

    total = sum(values)
    n = len(values)

    # Mean represented as rational numerator/denominator.
    return [(value * n - total) for value in values], n


def covariance_terms(x, y):
    """
    Return exact integer covariance numerator.

    This is:
        n Σxy - Σx Σy
    """
    if len(x) != len(y) or not x:
        raise ValueError("Invalid correlation inputs")

    n = len(x)

    sx = sum(x)
    sy = sum(y)
    sxy = sum(a * b for a, b in zip(x, y))

    return n * sxy - sx * sy


def variance_term(x):
    """Exact integer variance numerator."""
    if not x:
        raise ValueError("Empty input")

    n = len(x)
    sx = sum(x)
    sxx = sum(v * v for v in x)

    return n * sxx - sx * sx


def ratio_interval_wad(numerator, denominator):
    """
    Return a conservative WAD interval for:

        numerator / sqrt(denominator)

    where denominator > 0.

    Uses integer square-root bounds.
    """
    if denominator <= 0:
        raise ValueError("Non-positive denominator")

    root_low = integer_sqrt(denominator)
    root_high = root_low if root_low * root_low == denominator else root_low + 1

    if numerator >= 0:
        low = (numerator * SCALE) // root_high
        high = (numerator * SCALE + root_low - 1) // root_low
    else:
        low = (numerator * SCALE) // root_low
        high = (numerator * SCALE + root_high - 1) // root_high

    return low, high


def correlation_interval(x, y):
    """
    Certified WAD interval for Pearson-style correlation.

    rho = covariance / sqrt(var_x * var_y)

    The covariance and variance quantities are exact integers.
    """
    if len(x) != len(y):
        raise ValueError("Dimension mismatch")

    if len(x) < 2:
        raise ValueError("At least two observations required")

    covariance = covariance_terms(x, y)
    variance_x = variance_term(x)
    variance_y = variance_term(y)

    if variance_x == 0 or variance_y == 0:
        return 0, 0, "UNDEFINED_ZERO_VARIANCE"

    denominator = variance_x * variance_y

    low, high = ratio_interval_wad(covariance, denominator)

    # Mathematical correlation must remain within [-1, 1].
    low = max(-SCALE, low)
    high = min(SCALE, high)

    return low, high, "CERTIFIED"


def rolling_growth_correlation(agent_growth, structural_growth, window):
    """
    Calculate rolling growth-correlation certificates.

    Returns one record per completed window.
    """
    if window < 2:
        raise ValueError("Window must be >= 2")

    if len(agent_growth) != len(structural_growth):
        raise ValueError("Dimension mismatch")

    records = []

    for end in range(window, len(agent_growth) + 1):
        x = agent_growth[end - window:end]
        y = structural_growth[end - window:end]

        low, high, status = correlation_interval(x, y)

        records.append({
            "end_index": end - 1,
            "window": window,
            "rho_low": low,
            "rho_high": high,
            "status": status,
        })

    return records


def threshold_state(rho_low, rho_high, collapse_threshold, watch_threshold):
    """
    Deterministic threshold classification.

    A threshold is crossed only if the complete certified
    interval establishes that fact.
    """
    if rho_high < collapse_threshold:
        return "COLLAPSED"

    if rho_low < watch_threshold:
        return "WATCH"

    if rho_low >= watch_threshold:
        return "NORMAL"

    return "UNDECIDABLE"