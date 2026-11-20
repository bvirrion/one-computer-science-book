"""Merge sort against insertion sort, timed on the author's laptop."""
import random
import time

from merge_sort import merge_sort


def insertion_sort(t):
    t = list(t)
    for i in range(1, len(t)):
        x, j = t[i], i - 1
        while j >= 0 and t[j] > x:
            t[j + 1] = t[j]
            j -= 1
        t[j + 1] = x
    return t


def best_time(f, t, repeat=3):
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        f(t)
        times.append(time.perf_counter() - start)
    return min(times)


if __name__ == "__main__":
    rng = random.Random(2)
    for n in [250, 500, 1000, 2000, 4000]:
        t = [rng.random() for _ in range(n)]
        merge_t, insert_t = best_time(merge_sort, t), best_time(insertion_sort, t)
        ratio = insert_t / merge_t
        print(f"n = {n:4}: merge {merge_t * 1000:7.2f} ms"
              f"   insertion {insert_t * 1000:8.2f} ms   ratio {ratio:5.1f}")
