def exactly_one(a, b, c):
    """1 when exactly one of the three bits is 1."""
    return int(a + b + c == 1)
