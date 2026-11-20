"""Exercise: the superkeys of a schema of n attributes whose only candidate key has k
attributes, counted by brute force against 2^(n - k)."""

from itertools import combinations


def superkeys(n, key):
    """Sets of attributes (0..n-1) that contain the key: they determine the tuple."""
    return [set(c) for size in range(n + 1) for c in combinations(range(n), size)
            if set(key) <= set(c)]


if __name__ == "__main__":
    for n in range(1, 7):
        for k in range(1, n + 1):
            assert len(superkeys(n, range(k))) == 2 ** (n - k)
    print("superkeys = 2^(n - k) for every n <= 6")
