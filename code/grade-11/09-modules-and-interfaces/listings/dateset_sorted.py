"""A set of dates, kept in a sorted list searched by halving.

Interface: empty(), from_dates(dates), add(s, d), contains(s, d), size(s).
"""
import bisect


def empty():
    """Return a new set of dates, with no date in it."""
    return []


def from_dates(dates):
    """Return a new set holding the dates of the iterable dates."""
    return sorted(set(dates))


def add(s, d):
    """Add the date d to s; nothing changes if d is already in s."""
    if not contains(s, d):
        bisect.insort(s, d)


def contains(s, d):
    """Return True when the date d is in s."""
    i = bisect.bisect_left(s, d)
    return i < len(s) and s[i] == d


def size(s):
    """Return the number of dates in s."""
    return len(s)
