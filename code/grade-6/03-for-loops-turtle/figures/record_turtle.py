"""Record the turtle drawings of grade 6, chapter 3, as .dat tables for the figures.

    python code/grade-6/03-for-loops-turtle/figures/record_turtle.py

Each turtle listing runs unchanged under code/shared/turtlerec; the star variants of the
weekend problem run stars.py with its two numbers replaced. The tables go to
figures/out/.
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "code" / "shared" / "turtlerec"))

from turtlerec import record, record_source  # noqa: E402

OUT = HERE / "out"
LISTINGS = ["square", "polygon", "star", "spiral", "row_of_squares"]
EXERCISES = ["triangle", "open_polygon", "octagon", "row_of_triangles"]
STARS = [(5, 1), (5, 2), (5, 3)]
STARS += [(8, k) for k in range(1, 8)] + [(12, k) for k in range(1, 12)]


def star_source(n, k):
    text = (HERE.parent / "listings" / "stars.py").read_text()
    text = re.sub(r"^n = \d+", f"n = {n}", text, flags=re.M)
    return re.sub(r"^k = \d+", f"k = {k}", text, flags=re.M)


def main():
    OUT.mkdir(exist_ok=True)
    for name in LISTINGS:
        record(HERE.parent / "listings" / f"{name}.py").write_dat(OUT / f"{name}.dat")
    for name in EXERCISES:
        record(HERE.parent / "exercises" / f"{name}.py").write_dat(OUT / f"{name}.dat")
    for n, k in STARS:
        record_source(star_source(n, k)).write_dat(OUT / f"star-{n}-{k}.dat")
    count = len(LISTINGS) + len(EXERCISES) + len(STARS)
    print(f"wrote {count} tables to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
