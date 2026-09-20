from deterministic_rng import DeterministicRNG
from dependence import dependence_proxy


def permutation_null(x_rows, y_values, repetitions=32, seed=42):
    rng = DeterministicRNG(seed)
    y = list(y_values)

    scores = []

    for _ in range(repetitions):
        shuffled = list(y)

        for i in range(len(shuffled) - 1, 0, -1):
            j = rng.next_u64() % (i + 1)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]

        scores.append(dependence_proxy(x_rows, shuffled))

    return scores


def empirical_p_value(observed, null_scores):
    if not null_scores:
        return 0

    exceed = sum(1 for x in null_scores if x >= observed)

    return (exceed + 1) * 10**18 // (len(null_scores) + 1)