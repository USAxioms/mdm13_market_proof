AGENT_DIM = 13
STRUCTURAL_DIM = 27
TOTAL_DIM = 40


def split_state(state):
    if len(state) != TOTAL_DIM:
        raise ValueError("state must contain exactly 40 dimensions")

    return state[:AGENT_DIM], state[AGENT_DIM:]


def combine_state(agent, structural):
    if len(agent) != AGENT_DIM:
        raise ValueError("agent state must contain 13 dimensions")

    if len(structural) != STRUCTURAL_DIM:
        raise ValueError("structural state must contain 27 dimensions")

    return list(agent) + list(structural)


def validate_state(state):
    if len(state) != TOTAL_DIM:
        raise ValueError("invalid MDM state dimension")

    if not all(isinstance(x, int) for x in state):
        raise TypeError("MDM state must be WAD integers")

    return True