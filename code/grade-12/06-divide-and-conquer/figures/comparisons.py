"""Write comparisons.dat: merge sort's comparisons on random input, n log2 n, n^2/2."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from merge_sort import merge_sort  # noqa: E402

rng = random.Random(1)
with open(Path(__file__).with_suffix(".dat"), "w") as out:
    out.write("n merge nlogn half_square\n")
    for h in range(1, 14):
        n = 2 ** h
        count = merge_sort(rng.sample(range(n), n))[1]
        out.write(f"{n} {count} {n * h} {n * n // 2}\n")
