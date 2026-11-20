def agree(f, g):
    """True when the two-input functions f and g give the same bit on every input."""
    for a in [0, 1]:
        for b in [0, 1]:
            if f(a, b) != g(a, b):
                return False
    return True
