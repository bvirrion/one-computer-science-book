"""Write counts.dat: worst-case comparisons of linear search and insertion sort."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from count_insertion import insertion_sort  # noqa: E402
from count_linear import search  # noqa: E402

with open(Path(__file__).with_suffix(".dat"), "w") as out:
    out.write("n linear quadratic\n")
    for n in range(0, 101, 5):
        linear = search(list(range(n)), -1)[1]
        quadratic = insertion_sort(list(range(n, 0, -1)))
        out.write(f"{n} {linear} {quadratic}\n")
