import sys
sys.path.insert(0, "src")

from deterministic_rng import DeterministicRNG


def test_rng_repeatability():
    a = DeterministicRNG(42)
    b = DeterministicRNG(42)

    assert [a.next_u64() for _ in range(20)] == [
        b.next_u64() for _ in range(20)
    ]