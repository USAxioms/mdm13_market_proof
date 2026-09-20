import sys
sys.path.insert(0, "src")

from leakage import detect_temporal_identity


def test_no_identity_leakage():
    states = [[1, 2, 3, 4]]
    targets = [[9, 8]]

    assert detect_temporal_identity(states, targets) is False