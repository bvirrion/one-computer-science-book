"""The weekend problem, part I and II: comparisons when there is no duplicate."""
import random

from duplicates import Counted, by_pairs, by_sorting


def comparisons(find, values):
    Counted.count = 0
    assert not find([Counted(v) for v in values])
    return Counted.count


rng = random.Random(2026)
last_loss = 1                     # the last n where pairs did not lose
for n in range(2, 101):
    values = rng.sample(range(10 * n), n)       # n different values, shuffled
    pairs = comparisons(by_pairs, values)
    sorting = comparisons(by_sorting, values)
    if sorting >= pairs:
        last_loss = n
    if n in (2, 5, 10, 20, 50, 100):
        print(f"n = {n:3}: pairs {pairs:5}   sort then scan {sorting:4}")
print("sort then scan needs fewer comparisons from n =", last_loss + 1, "up to 100")
for n in (1000, 10**5):
    values = rng.sample(range(10 * n), n)
    print(f"n = {n}: pairs {n * (n - 1) // 2} (by the formula)   sort then scan",
          comparisons(by_sorting, values))
