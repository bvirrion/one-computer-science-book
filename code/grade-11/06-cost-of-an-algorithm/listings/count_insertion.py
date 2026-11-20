"""Insertion sort, counting the comparisons between elements."""
import random


def insertion_sort(t):
    comparisons = 0
    for i in range(1, len(t)):
        x, j = t[i], i
        while j > 0:
            comparisons += 1
            if t[j - 1] <= x:
                break
            t[j] = t[j - 1]
            j -= 1
        t[j] = x
    return comparisons


if __name__ == "__main__":
    rng = random.Random(6)
    print("    n   sorted  shuffled  reversed   n(n-1)/2")
    for n in [10, 100, 1000]:
        shuffled = rng.sample(range(n), n)
        counts = [insertion_sort(t) for t in
                  (list(range(n)), shuffled, list(range(n, 0, -1)))]
        print(f"{n:5} {counts[0]:8} {counts[1]:9} {counts[2]:9} {n * (n - 1) // 2:10}")
