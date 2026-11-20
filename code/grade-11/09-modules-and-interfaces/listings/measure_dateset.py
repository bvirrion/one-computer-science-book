"""Time contains(s, d) in the three implementations, for n dates."""
import statistics
import time
from datetime import date, timedelta

import dateset_list
import dateset_set
import dateset_sorted

START = date(1800, 1, 1)


def per_lookup(ds, s, targets, runs=5, repeat=10):
    times = []
    for _ in range(runs):
        begin = time.perf_counter()
        for _ in range(repeat):
            for d in targets:
                ds.contains(s, d)
        times.append((time.perf_counter() - begin) / (repeat * len(targets)))
    return statistics.median(times)


if __name__ == "__main__":
    print(f"{'n':>7} {'list':>10} {'sorted':>10} {'set':>10}   (per lookup)")
    for n in [1000, 10_000, 100_000]:
        days = [START + timedelta(days=2 * i) for i in range(n)]   # one day in two
        targets = [days[-1], days[-1] - timedelta(days=1)]   # present, absent
        row = []
        for ds in [dateset_list, dateset_sorted, dateset_set]:
            s = ds.from_dates(days)
            row.append(per_lookup(ds, s, targets))
        print(f"{n:>7}", " ".join(f"{t * 1e6:8.2f} us" for t in row))
    print(f"at n = 100000, the set is {row[0] / row[2]:,.0f} times faster",
          "than the list")
