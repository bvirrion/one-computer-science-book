"""timing.py: the same three algorithms timed, best of five runs."""

import random
import time

from count_ops import insertion_sort
from sorts import maximum, merge_sort


def best_time(f, a):
    best = float("inf")
    for _ in range(5):
        b = list(a)
        start = time.perf_counter()
        f(b)
        best = min(best, time.perf_counter() - start)
    return best


rng = random.Random(2026)
algorithms = [lambda a: maximum(a, [0]), lambda a: merge_sort(a, [0]), insertion_sort]
previous = None
print(f"{'n':>5} {'max (ms)':>9} {'merge (ms)':>10} {'ins. (ms)':>10}   ratios")
for n in [500, 1000, 2000, 4000, 8000]:
    a = rng.sample(range(10 * n), n)
    times = [1000 * best_time(f, a) for f in algorithms]
    ratios = "" if previous is None else " ".join(
        f"{t / p:5.2f}" for t, p in zip(times, previous))
    t1, t2, t3 = times
    print(f"{n:5d} {t1:9.3f} {t2:10.3f} {t3:10.1f}   {ratios}".rstrip())
    previous = times
