def mean(t):
    """Return the mean of the non-empty list of numbers t.

    >>> mean([2, 4, 9])
    5.0
    >>> mean([7])
    7.0
    >>> mean([0.5, 0.25])
    0.375
    """
    return sum(t) / len(t)
