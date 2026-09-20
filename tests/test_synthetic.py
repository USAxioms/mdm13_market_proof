import sys
sys.path.insert(0, "src")

from synthetic import generate


def test_dimensions():
    rows = generate(10, 42, "NULL")

    assert len(rows) == 10
    assert len(rows[0]["agent"]) == 13
    assert len(rows[0]["structural"]) == 27
    assert len(rows[0]["state"]) == 40