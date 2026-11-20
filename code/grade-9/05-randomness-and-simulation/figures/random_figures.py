"""Data for the chapter's charts.

    python code/grade-9/05-randomness-and-simulation/figures/random_figures.py

frequency.dat comes from the captured output of frequencies.py; walk.dat is the path
of random_walk.py, rebuilt with its own function and seed; points.dat holds 1,000
points of the square, drawn with the generator of estimate_pi.py and its seed.
"""

import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parent
sys.path.insert(0, str(CHAPTER / "listings"))

from random_walk import walk  # noqa: E402

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

rows = ["throws frequency"]
for line in (CHAPTER / "outputs" / "frequencies.txt").read_text().splitlines()[2:]:
    words = line.split()
    if len(words) == 3 and words[0].isdigit():
        rows.append(f"{words[0]} {words[2]}")
(OUT / "frequency.dat").write_text("\n".join(rows) + "\n")

random.seed(11)
path = walk(100)
(OUT / "walk.dat").write_text(
    "step position\n" + "".join(f"{k} {p}\n" for k, p in enumerate(path)))

random.seed(8)
lines = ["x y inside"]
for _ in range(1000):
    x = random.random()
    y = random.random()
    lines.append(f"{x:.4f} {y:.4f} {1 if x * x + y * y <= 1 else 0}")
(OUT / "points.dat").write_text("\n".join(lines) + "\n")
