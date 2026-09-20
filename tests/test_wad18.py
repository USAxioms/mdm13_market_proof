import sys
sys.path.insert(0, "src")

from wad18 import *


def test_add():
    assert add(from_int(2), from_int(3)) == from_int(5)


def test_mul():
    assert mul(from_int(2), from_int(3)) == from_int(6)


def test_div():
    assert div(from_int(6), from_int(3)) == from_int(2)


def test_exact_decimal():
    x = 123456789012345678
    assert mul(x, from_int(1)) == x