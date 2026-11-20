"""A set of dates, kept in a Python set.

Interface: empty(), from_dates(dates), add(s, d), contains(s, d), size(s).
"""


def empty():
    """Return a new set of dates, with no date in it."""
    return set()


def from_dates(dates):
    """Return a new set holding the dates of the iterable dates."""
    return set(dates)


def add(s, d):
    """Add the date d to s; nothing changes if d is already in s."""
    s.add(d)


def contains(s, d):
    """Return True when the date d is in s."""
    return d in s


def size(s):
    """Return the number of dates in s."""
    return len(s)
