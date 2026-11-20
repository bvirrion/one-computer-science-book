"""nodes.py: nodes.dat for the chart, from outputs/queens.txt."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
lines = (HERE.parent / "outputs" / "queens.txt").read_text().splitlines()
rows = [line.split() for line in lines if line.split() and line.split()[0].isdigit()]
with open(HERE / "nodes.dat", "w") as f:
    f.write("n solutions pruned full ratio\n")
    for r in rows:
        f.write(" ".join(r) + "\n")
