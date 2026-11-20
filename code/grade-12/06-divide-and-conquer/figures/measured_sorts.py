"""Write measured_sorts.dat: milliseconds for merge sort and insertion sort."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from measure_sorts import best_time, insertion_sort  # noqa: E402
from merge_sort import merge_sort  # noqa: E402

rng = random.Random(2)
with open(Path(__file__).with_suffix(".dat"), "w") as out:
    out.write("n merge insertion\n")
    for n in [250, 500, 1000, 2000, 3000, 4000, 6000, 8000]:
        t = [rng.random() for _ in range(n)]
        out.write(f"{n} {best_time(merge_sort, t) * 1000:.3f}"
                  f" {best_time(insertion_sort, t) * 1000:.3f}\n")
