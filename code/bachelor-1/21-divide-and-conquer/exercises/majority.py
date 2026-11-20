"""majority.py: the key held by more than half of a list, by divide and conquer."""


def majority(a):
    """The majority key of a, or None."""
    if len(a) == 1:
        return a[0]
    mid = len(a) // 2
    candidates = {majority(a[:mid]), majority(a[mid:])} - {None}
    for c in candidates:  # a majority of a is a majority of one half
        if 2 * a.count(c) > len(a):
            return c
    return None
