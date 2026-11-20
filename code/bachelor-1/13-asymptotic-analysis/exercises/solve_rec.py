"""solve_rec.py: T(n) = a T(n/b) + n^k computed for powers of b, and its growth
read from the numbers: the exponent of T, and whether a log factor remains."""

from math import log


def values(a, b, k, levels):
    """T(b^0), ..., T(b^levels), with T(1) = 1."""
    t = [1]
    for i in range(1, levels + 1):
        t.append(a * t[-1] + b ** (i * k))
    return t


def identify(a, b, k, levels=40):
    """Estimates the exponent e of T from the last two values, and says which
    case of the master theorem the numbers show."""
    t = values(a, b, k, levels)
    e = log(t[-1] / t[-2], b)  # T(bn) / T(n) is about b^e
    if abs(e - k) > 0.05 and e > k:
        return "leaves", e
    # n^k times log n: T(n) / n^k grows by about one each level
    growth = t[-1] / b ** (levels * k) - t[-2] / b ** ((levels - 1) * k)
    return ("even" if growth > 0.5 else "root"), e
