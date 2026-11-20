"""Brute force against merging, timed on the author's laptop."""
import time

from inversions import compare, inversions_brute, ranking, sort_count


def timed(f, t):
    start = time.perf_counter()
    result = f(t)
    return result, time.perf_counter() - start


for n in [1000, 2000, 4000, 8000]:
    t = compare(ranking(n, 1), ranking(n, 2))
    brute, t_brute = timed(inversions_brute, t)
    (_, merged), t_merge = timed(sort_count, t)
    print(f"n = {n:4}: brute {t_brute:6.3f} s   merging {t_merge:6.3f} s"
          f"   ratio {t_brute / t_merge:5.0f}   same count: {brute == merged}")
_, t_merge = timed(sort_count, compare(ranking(100_000, 1), ranking(100_000, 2)))
print(f"n = 100000: merging {t_merge:.2f} s")
