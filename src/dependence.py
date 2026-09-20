from collections import defaultdict
from wad18 import SCALE


def sign_bin(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def joint_counts(x_rows, y_values):
    counts = defaultdict(int)

    for x, y in zip(x_rows, y_values):
        xb = tuple(sign_bin(v) for v in x)
        yb = sign_bin(y)
        counts[(xb, yb)] += 1

    return counts


def dependence_proxy(x_rows, y_values):
    """
    Deterministic WAD-compatible dependence proxy.

    This is intentionally NOT called mutual information.

    It measures normalized signed-bin co-occurrence relative to
    marginal frequencies.
    """

    if len(x_rows) != len(y_values):
        raise ValueError("length mismatch")

    n = len(y_values)

    if n == 0:
        return 0

    x_counts = defaultdict(int)
    y_counts = defaultdict(int)
    joint = defaultdict(int)

    for x, y in zip(x_rows, y_values):
        xb = tuple(sign_bin(v) for v in x)
        yb = sign_bin(y)

        x_counts[xb] += 1
        y_counts[yb] += 1
        joint[(xb, yb)] += 1

    score = 0

    for (xb, yb), count in joint.items():
        expected_num = x_counts[xb] * y_counts[yb]

        if expected_num == 0:
            continue

        observed = count * n
        diff = abs(observed - expected_num)

        score += (diff * SCALE) // expected_num

    return score // max(1, len(joint))


def conditional_dependence_proxy(x_rows, z_rows, y_values):
    """
    Deterministic conditional residual-style proxy.

    Conditioning is performed by exact integer group means.
    """

    if not (len(x_rows) == len(z_rows) == len(y_values)):
        raise ValueError("length mismatch")

    groups = defaultdict(list)

    for z, y in zip(z_rows, y_values):
        key = tuple(sign_bin(v) for v in z)
        groups[key].append(y)

    residual_y = []

    for z, y in zip(z_rows, y_values):
        key = tuple(sign_bin(v) for v in z)
        group = groups[key]
        baseline = sum(group) // len(group)
        residual_y.append(y - baseline)

    return dependence_proxy(x_rows, residual_y)