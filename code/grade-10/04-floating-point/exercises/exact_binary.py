"""Exercise 7: the exact binary expansion of a float, which always ends."""
from fractions import Fraction


def exact_binary(x):
    """Return all the binary digits after the point of the float x, 0 <= x < 1."""
    q = Fraction(x)
    digits = ""
    while q != 0:
        q = 2 * q
        digits += "1" if q >= 1 else "0"
        if q >= 1:
            q -= 1
    return digits
