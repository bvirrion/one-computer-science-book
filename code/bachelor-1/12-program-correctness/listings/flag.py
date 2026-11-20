"""flag.py: the three-colour flag: sort a list of 0, 1, 2 in one pass."""


def flag(a):
    """Rearranges a so that all 0s come first, then 1s, then 2s; returns the swaps."""
    low, mid, high = 0, 0, len(a)
    swaps = 0
    while mid < high:
        # invariant: a[:low] == 0, a[low:mid] == 1, a[mid:high] unknown, a[high:] == 2
        if a[mid] == 0:
            a[low], a[mid] = a[mid], a[low]
            low, mid, swaps = low + 1, mid + 1, swaps + 1
        elif a[mid] == 1:
            mid += 1
        else:
            high -= 1
            a[mid], a[high] = a[high], a[mid]
            swaps += 1
    return swaps  # mid == high: the unknown region is empty


if __name__ == "__main__":
    a = [2, 0, 1, 2, 1, 0, 0, 2, 1]
    swaps = flag(a)
    print(a, swaps, "swaps")
