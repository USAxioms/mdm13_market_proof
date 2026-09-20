def detect_direct_leakage(predictors, targets):
    """
    Detects exact target duplication in predictor vectors.
    """

    target_set = set(targets)

    for row in predictors:
        if any(value in target_set for value in row):
            return True

    return False


def detect_temporal_identity(states, targets):
    """
    Detects the prohibited construction where target is literally a
    predictor slice at the same timestep.
    """

    for state, target in zip(states, targets):
        if isinstance(target, list) and target == state[:len(target)]:
            return True

    return False