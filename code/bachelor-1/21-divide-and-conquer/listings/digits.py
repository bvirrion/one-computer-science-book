"""digits.py: long numbers as lists of decimal digits, least significant first,
with a counter of digit products."""

products = 0  # digit products since the last reset


def to_digits(x, n):
    """The n lowest digits of x >= 0, least significant first."""
    return [x // 10**i % 10 for i in range(n)]


def from_digits(d):
    return sum(v * 10**i for i, v in enumerate(d))


def normalise(r):
    """Propagate carries in place: every cell back to 0..9 (cells may be negative)."""
    carry = 0
    for i in range(len(r)):
        carry, r[i] = divmod(r[i] + carry, 10)
    assert carry == 0, "the result does not fit"
    return r


def school(a, b):
    """The school method: every digit of a times every digit of b."""
    global products
    r = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
        products += len(b)
    return normalise(r)
