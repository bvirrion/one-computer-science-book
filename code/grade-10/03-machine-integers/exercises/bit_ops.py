"""Exercise 8: test, set and clear one bit of a whole number."""


def test_bit(x, i):
    """Return True when bit i of x (bit 0 is the rightmost) is 1."""
    return (x >> i) & 1 == 1


def set_bit(x, i):
    """Return x with bit i set to 1."""
    return x | (1 << i)


def clear_bit(x, i):
    """Return x with bit i set to 0."""
    return x & ~(1 << i)
