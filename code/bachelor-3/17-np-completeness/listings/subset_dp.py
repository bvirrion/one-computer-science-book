"""subset_dp.py -- subset sum by dynamic programming: the set of reachable sums grows
with the target T, so the table has up to n x (T + 1) cells. Polynomial in T, but T has
only about b bits: exponential in the size of the input."""
import random


def dp_cells(numbers, target):
    """Decide subset sum; count the (number, sum) cells the table fills."""
    reachable, cells = [True] + [False] * target, 0
    for x in numbers:
        for s in range(target, x - 1, -1):  # downwards: each number used once
            cells += 1
            if reachable[s - x]:
                reachable[s] = True
    return reachable[target], cells


if __name__ == "__main__":
    rng = random.Random(17)
    n = 20
    print(f"n = {n} numbers of b bits; target = half their sum")
    print(" b   input bits   target T   table cells   found")
    for b in (4, 8, 12, 16):
        numbers = [rng.randrange(1, 2 ** b) for _ in range(n)]
        target = sum(numbers) // 2
        found, cells = dp_cells(numbers, target)
        print(f"{b:>2}   {n * b:>10}   {target:>8,}   {cells:>11,}   {found}")
