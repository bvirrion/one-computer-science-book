"""search_vs_verify.py -- subset sum with no solution: an exhaustive search computes the
sum of every subset, 2^n of them; checking one certificate costs at most n steps."""
import random


def search(numbers, target):
    """All subset sums, built one number at a time; returns (found, sums computed)."""
    sums, computed = [0], 1
    for x in numbers:
        sums = sums + [s + x for s in sums]
        computed += len(sums) // 2
    return target in sums, computed


if __name__ == "__main__":
    rng = random.Random(16)
    print(" n   search: sums computed   verify: steps")
    for n in range(4, 23, 2):
        numbers = [2 * rng.randrange(1, 10**6) for _ in range(n)]  # all even
        found, computed = search(numbers, 2 * 10**6 + 1)  # an odd target: never found
        assert not found and computed == 2 ** n
        print(f"{n:>2}   {computed:>21,}   {n:>13}")
