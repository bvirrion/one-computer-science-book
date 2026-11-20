"""Exercise 15: the largest reading, when a missing reading is NaN."""
import math


def largest_buggy(readings):
    best = readings[0]
    for r in readings:
        if r > best:
            best = r
    return best


def largest(readings):
    """Return the largest reading that is not NaN (there must be one)."""
    values = [r for r in readings if not math.isnan(r)]
    assert values, "no reading"
    best = values[0]
    for r in values:
        if r > best:
            best = r
    return best
