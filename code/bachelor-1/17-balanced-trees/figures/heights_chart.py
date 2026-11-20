"""heights_chart.py: heights.dat for the chart, from outputs/heights.txt."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
lines = (HERE.parent / "outputs" / "heights.txt").read_text().splitlines()
rows = [line.split() for line in lines if line.split() and line.split()[0].isdigit()]
with open(HERE / "heights.dat", "w") as f:
    f.write("n catalogue sorted shuffled avl llrb lg\n")
    for r in rows:
        f.write(" ".join(r) + "\n")
