SCALE = 10**18
HALF = SCALE // 2


def wad(value: int) -> int:
    if isinstance(value, bool):
        raise TypeError("boolean is not valid WAD")
    return int(value)


def from_int(value: int) -> int:
    return value * SCALE


def to_int(x: int) -> int:
    if x >= 0:
        return x // SCALE
    return -((-x) // SCALE)


def add(a: int, b: int) -> int:
    return a + b


def sub(a: int, b: int) -> int:
    return a - b


def neg(a: int) -> int:
    return -a


def mul(a: int, b: int) -> int:
    product = a * b
    sign = -1 if product < 0 else 1
    n = abs(product)

    q, r = divmod(n, SCALE)

    if r * 2 >= SCALE:
        q += 1

    return sign * q


def div(a: int, b: int) -> int:
    if b == 0:
        raise ZeroDivisionError("WAD division by zero")

    sign = -1 if (a < 0) ^ (b < 0) else 1
    n = abs(a) * SCALE
    d = abs(b)

    q, r = divmod(n, d)

    if r * 2 >= d:
        q += 1

    return sign * q


def abs_wad(a: int) -> int:
    return abs(a)


def clamp(a: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, a))


def mean(values):
    if not values:
        return 0
    return div(sum(values), from_int(len(values)))


def square(a: int) -> int:
    return mul(a, a)