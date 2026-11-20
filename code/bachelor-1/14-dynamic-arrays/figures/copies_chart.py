"""copies_chart.py: the 17 pushes of vec_demo.c (its captured output) as a table:
size, capacity, actual cost (one write plus the copies), potential, amortised cost."""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
text = (HERE.parent / "outputs" / "vec_demo.txt").read_text()
PUSH = r"push +(\d+): size +(\d+) +capacity +(\d+) +copies so far +(\d+)"

with open(HERE / "copies.dat", "w") as f:
    f.write("i size capacity cost phi amortised\n")
    copies, phi = 0, 2 * 0 - 1  # the empty array has capacity 1
    for row in re.findall(PUSH, text):
        i, size, capacity, total = map(int, row)
        cost = 1 + total - copies
        new_phi = 2 * size - capacity
        f.write(f"{i} {size} {capacity} {cost} {new_phi} {cost + new_phi - phi}\n")
        copies, phi = total, new_phi
