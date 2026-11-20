import math


def count_tenths():
    """Count the steps of 0.1 from 0 to 1, with a tolerance (fixed loop)."""
    x = 0.0
    steps = 0
    while not math.isclose(x, 1.0):
        x = x + 0.1
        steps = steps + 1
    return steps
