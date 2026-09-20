import sys
sys.path.insert(0, "src")

from ablation import incremental_gain


def test_gain():
    assert incremental_gain(20, 5) == 15
