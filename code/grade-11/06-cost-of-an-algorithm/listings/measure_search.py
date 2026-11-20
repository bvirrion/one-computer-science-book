"""One lookup in a million numbers: a list, binary search, a set."""
import bisect
import statistics
import time

N = 10**6
numbers = list(range(0, 2 * N, 2))       # sorted, even numbers only
as_set = set(numbers)
targets = [N + 1, 2 * N - 2]             # absent (odd), and the very last one


def per_lookup(found, runs=5, repeat=20):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        for _ in range(repeat):
            for x in targets:
                found(x)
        times.append((time.perf_counter() - start) / (repeat * len(targets)))
    return statistics.median(times)


def in_sorted(x):
    i = bisect.bisect_left(numbers, x)
    return i < len(numbers) and numbers[i] == x


for name, found in [("x in list", lambda x: x in numbers),
                    ("binary search", in_sorted),
                    ("x in set", lambda x: x in as_set)]:
    print(f"{name:14} {per_lookup(found) * 1e6:10.3f} microseconds per lookup")
