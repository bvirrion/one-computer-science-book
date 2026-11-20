def search(t, x):
    """Pre: t is sorted. Post: an index i with t[i] == x, or None if x is not in t."""
    lo, hi = 0, len(t)
    while lo < hi:
        # invariant: x is neither in t[:lo] nor in t[hi:]; variant: hi - lo
        mid = (lo + hi) // 2
        print(f"  lo={lo} mid={mid} hi={hi}")
        if t[mid] == x:
            return mid
        if t[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return None


t = [3, 8, 12, 15, 21, 30, 34, 41, 47, 52]
for x in [41, 3, 20]:
    print("search", x)
    print("->", search(t, x))
