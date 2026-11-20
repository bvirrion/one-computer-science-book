"""quickselect.py: the k-th smallest key with a random pivot, comparisons counted."""
import random

from town import people


def quickselect(a, k, rng, count):
    """The key of rank k (0 for the smallest) of the list a of distinct keys."""
    while True:
        pivot = a[rng.randrange(len(a))]
        count[0] += len(a) - 1
        smaller = [x for x in a if x < pivot]
        if k < len(smaller):
            a = smaller
        elif k == len(smaller):
            return pivot
        else:
            k -= len(smaller) + 1
            a = [x for x in a if x > pivot]


if __name__ == "__main__":
    names = sorted(people())
    n = len(names)
    for k in [0, n // 2, n - 1]:
        counts = []
        for seed in range(1000):
            count = [0]
            assert quickselect(names, k, random.Random(seed), count) == names[k]
            counts.append(count[0])
        print(f"rank {k:3}: mean {sum(counts) / 1000:6.1f} comparisons,"
              f" largest {max(counts)}; 4n = {4 * n}")
