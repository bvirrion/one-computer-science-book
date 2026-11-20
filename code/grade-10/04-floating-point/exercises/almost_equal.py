"""Exercise 11: closeness with a relative and an absolute tolerance."""


def almost_equal(a, b, rel=1e-9, abs_=0.0):
    """True when |a - b| <= max(rel * max(|a|, |b|), abs_), like math.isclose."""
    return abs(a - b) <= max(rel * max(abs(a), abs(b)), abs_)
