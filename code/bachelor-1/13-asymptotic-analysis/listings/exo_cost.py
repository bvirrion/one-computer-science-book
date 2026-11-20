"""exo_cost.py: exercise 6, a loop whose inner part depends on i."""

from math import log2


def doublings(n):
    count = 0
    for i in range(1, n + 1):
        j = i
        while j < n:  # "at most log2 n times, so n log2 n in all"
            j *= 2
            count += 1
    return count


if __name__ == "__main__":
    for n in [2**10, 2**13, 2**16]:
        c = doublings(n)
        print(f"n={n:6d}  count={c:7d}  count/n={c / n:.3f}  "
              f"count/(n log2 n)={c / (n * log2(n)):.3f}")
