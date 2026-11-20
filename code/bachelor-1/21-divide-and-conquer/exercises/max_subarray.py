"""max_subarray.py: the largest sum of a non-empty slice, by divide and conquer."""


def best(a, lo=0, hi=None):
    """The largest sum of a non-empty slice of a[lo:hi]."""
    if hi is None:
        hi = len(a)
    if hi - lo == 1:
        return a[lo]
    mid = (lo + hi) // 2
    left_end, s = a[mid - 1], 0  # best slice ending at mid - 1
    for i in range(mid - 1, lo - 1, -1):
        s += a[i]
        left_end = max(left_end, s)
    right_start, s = a[mid], 0  # best slice starting at mid
    for i in range(mid, hi):
        s += a[i]
        right_start = max(right_start, s)
    return max(best(a, lo, mid), best(a, mid, hi), left_end + right_start)


def kadane(a):
    ending_here = result = a[0]
    for x in a[1:]:
        ending_here = max(x, ending_here + x)
        result = max(result, ending_here)
    return result
