from wad18 import SCALE


def correlation_like_metric(dim):
    """
    Deterministic candidate metric.

    Diagonal = 1 WAD.
    Off-diagonal = 0 WAD.

    This is a baseline positive-definite metric rather than an assertion
    that this is the true market metric.
    """

    return [
        [
            SCALE if i == j else 0
            for j in range(dim)
        ]
        for i in range(dim)
    ]


def metric_perturbation(metric, amount):
    result = [row[:] for row in metric]

    for i in range(len(result)):
        result[i][i] -= amount

    return result