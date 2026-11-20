"""Write measured_plot.dat: insertion sort on shuffled lists, median of five runs."""
import random
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from count_insertion import insertion_sort  # noqa: E402

rng = random.Random(1)
with open(Path(__file__).with_suffix(".dat"), "w") as out:
    out.write("n ms\n")
    for n in range(500, 4001, 500):
        times = []
        for _ in range(5):
            t = rng.sample(range(n), n)
            start = time.perf_counter()
            insertion_sort(t)
            times.append(time.perf_counter() - start)
        out.write(f"{n} {statistics.median(times) * 1000:.2f}\n")
