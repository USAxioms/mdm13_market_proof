from wad18 import SCALE
from deterministic_rng import DeterministicRNG
from state import combine_state
from target import independent_target


def generate(samples=256, seed=42, mode="NULL"):
    rng = DeterministicRNG(seed)

    agent = [0] * 13
    structural = [0] * 27

    rows = []

    for _ in range(samples):
        agent = [
            (x * 8) // 10 + rng.signed(SCALE // 20)
            for x in agent
        ]

        structural = [
            (x * 7) // 10 + rng.signed(SCALE // 20)
            for x in structural
        ]

        if mode in ("SIGNAL_13", "INTERACTION_13_27"):
            structural[0] += agent[0] // 2

        if mode == "SIGNAL_27":
            agent[0] += structural[0] // 2

        state = combine_state(agent, structural)
        target = independent_target(agent, structural, mode)

        rows.append({
            "agent": list(agent),
            "structural": list(structural),
            "state": state,
            "target": target
        })

    return rows