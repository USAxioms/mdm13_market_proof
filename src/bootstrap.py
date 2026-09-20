def bootstrap_interval(values):
    """
    Deterministic percentile-free interval based on min/max.
    This is intentionally conservative and does not claim a classical
    statistical confidence interval.
    """

    if not values:
        return 0, 0

    ordered = sorted(values)

    return ordered[0], ordered[-1]