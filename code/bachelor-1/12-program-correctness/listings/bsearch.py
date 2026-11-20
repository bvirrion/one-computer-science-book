"""bsearch.py: binary search on the half-open interval [lo, hi) of a sorted list."""


def leftmost(a, x):
    """Precondition: a sorted. Returns the least i with a[i] >= x (len(a) if none):
    the position of the first x if x is present, where to insert it otherwise."""
    lo, hi = 0, len(a)
    while lo < hi:
        # invariant: a[:lo] < x <= a[hi:], and 0 <= lo <= hi <= len(a)
        mid = lo + (hi - lo) // 2  # lo <= mid < hi
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo  # lo == hi: a[:lo] < x <= a[lo:]


if __name__ == "__main__":
    a = [2, 3, 3, 3, 7, 9]
    for x in [3, 2, 9, 5, 1, 10]:
        i = leftmost(a, x)
        found = i < len(a) and a[i] == x
        print(f"x={x:2}: leftmost {i}, {'found' if found else 'absent'}")
    print("empty list:", leftmost([], 4))
