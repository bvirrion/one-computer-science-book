"""Exercise 15: Jaccard similarity of two sets."""
from fractions import Fraction


def jaccard(a, b):
    """Return |a & b| / |a | b| as a fraction; precondition: a | b is not empty."""
    assert a | b, "two empty sets have no Jaccard index"
    return Fraction(len(a & b), len(a | b))
