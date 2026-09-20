import sys
sys.path.insert(0, "src")

from dependence import dependence_proxy


def test_identical_signal_has_dependence():
    x = [[i] for i in range(-10, 11)]
    y = [i for i in range(-10, 11)]

    assert dependence_proxy(x, y) > 0