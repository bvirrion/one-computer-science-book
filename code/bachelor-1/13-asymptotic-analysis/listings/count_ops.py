"""count_ops.py: insertion sort, instrumented to count its comparisons."""

import random


def insertion_sort(a):
    """Sorts a in place and returns the number of comparisons between elements."""
    comparisons = 0
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0:
            comparisons += 1
            if a[j] <= key:
                break
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return comparisons


if __name__ == "__main__":
    rng = random.Random(13)
    print(f"{'n':>5} {'sorted':>7} {'reversed':>9} {'random':>7} {'n(n-1)/4':>9}")
    for n in [8, 16, 32, 64, 128, 256, 512]:
        best = insertion_sort(list(range(n)))
        worst = insertion_sort(list(range(n, 0, -1)))
        middle = insertion_sort(rng.sample(range(n), n))
        print(f"{n:5d} {best:7d} {worst:9d} {middle:7d} {n * (n - 1) / 4:9.0f}")
