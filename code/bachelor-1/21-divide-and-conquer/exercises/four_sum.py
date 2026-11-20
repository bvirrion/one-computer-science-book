"""four_sum.py: positions i < j < k < m with a[i] + a[j] + a[k] + a[m] == target,
by meeting in the middle on the sums of pairs: O(n^2 log n)."""

from bisect import bisect_left


def four_sum(a, target):
    """Positions (i, j, k, m), i < j < k < m, of a solution, or None."""
    n = len(a)
    latest = {}  # sum -> the pair (k, m) with that sum and the largest k
    for k in range(n):
        for m in range(k + 1, n):
            latest[a[k] + a[m]] = (k, m)  # k grows: the last kept is the latest
    sums = sorted(latest)
    for i in range(n):
        for j in range(i + 1, n):
            want = target - a[i] - a[j]
            p = bisect_left(sums, want)
            if p < len(sums) and sums[p] == want and latest[want][0] > j:
                return (i, j) + latest[want]
    return None
