"""rightmost.py: one past the last occurrence of x in a sorted list."""


def rightmost(a, x):
    """Precondition: a sorted. Returns the least i with a[i] > x (len(a) if none)."""
    lo, hi = 0, len(a)
    while lo < hi:
        # invariant: a[:lo] <= x < a[hi:], and 0 <= lo <= hi <= len(a)
        mid = lo + (hi - lo) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo
