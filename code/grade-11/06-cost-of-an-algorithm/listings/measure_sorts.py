"""Running times of insertion sort when n doubles: the median of five runs."""
import random
import statistics
import time

from count_insertion import insertion_sort


def median_time(n, rng, runs=5):
    times = []
    for _ in range(runs):
        t = rng.sample(range(n), n)       # a new shuffled list for each run
        start = time.perf_counter()
        insertion_sort(t)
        times.append(time.perf_counter() - start)
    return statistics.median(times)


rng = random.Random(1)
previous = None
for n in [1000, 2000, 4000]:
    seconds = median_time(n, rng)
    ratio = f"   x {seconds / previous:.1f}" if previous else ""
    print(f"n = {n}: {seconds * 1000:7.1f} ms{ratio}")
    previous = seconds
