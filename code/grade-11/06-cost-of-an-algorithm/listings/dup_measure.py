"""The weekend problem, part III and IV: running times, median of three runs."""
import random
import statistics
import time

from duplicates import by_pairs, by_set, by_sorting


def seconds(find, values, runs=3):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        assert not find(values)
        times.append(time.perf_counter() - start)
    return statistics.median(times)


rng = random.Random(7)
pairs = {}
for n in (1000, 2000, 4000):
    values = rng.sample(range(10 * n), n)
    pairs[n] = seconds(by_pairs, values)
    print(f"n = {n:6}: pairs {pairs[n] * 1000:9.1f} ms")
values = rng.sample(range(10**6), 10**5)
sorting, hashing = seconds(by_sorting, values), seconds(by_set, values)
guess = pairs[4000] * (10**5 / 4000) ** 2           # a quadratic cost: x 625
print(f"n = 100000: sort then scan {sorting * 1000:.1f} ms,"
      f" set {hashing * 1000:.1f} ms")
print(f"pairs at n = 100000, from n = 4000 times 625: about {guess:.0f} s")
print(f"speed-up of sort then scan: about {guess / sorting:,.0f} times")
