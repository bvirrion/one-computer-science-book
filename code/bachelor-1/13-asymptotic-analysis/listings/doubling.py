"""doubling.py: comparison counts of three algorithms as n doubles."""

import random

from count_ops import insertion_sort
from sorts import maximum, merge_sort

rng = random.Random(2026)
previous = None
print(f"{'n':>5} {'maximum':>8} {'merge sort':>10} {'insertion':>10}   ratios")
for n in [500, 1000, 2000, 4000, 8000]:
    a = rng.sample(range(10 * n), n)
    c_max, c_merge = [0], [0]
    maximum(a, c_max)
    merge_sort(a, c_merge)
    counts = (c_max[0], c_merge[0], insertion_sort(list(a)))
    ratios = "" if previous is None else " ".join(
        f"{c / p:5.2f}" for c, p in zip(counts, previous))
    print(f"{n:5d} {counts[0]:8d} {counts[1]:10d} {counts[2]:10d}   {ratios}".rstrip())
    previous = counts
