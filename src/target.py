from wad18 import add, mul


def independent_target(agent, structural, mode):
    """
    Generates a target that is not a slice of the predictor state.

    The target is constructed from controlled ground truth rather than
    copying predictor dimensions.
    """

    if mode == "NULL":
        return 0

    if mode == "SIGNAL_13":
        return sum(mul(x, x) for x in agent) // max(1, len(agent))

    if mode == "SIGNAL_27":
        return sum(mul(x, x) for x in structural) // max(1, len(structural))

    if mode == "INTERACTION_13_27":
        total = 0
        for a, b in zip(agent, structural[:len(agent)]):
            total += mul(a, b)
        return total // max(1, len(agent))

    raise ValueError(f"unknown target mode: {mode}")