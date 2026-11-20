"""comparisons.py: comparisons.dat for the chart, from outputs/counts.txt."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
lines = (HERE.parent / "outputs" / "counts.txt").read_text().splitlines()
rows = [line.split() for line in lines if line.split() and line.split()[0].isdigit()]
with open(HERE / "comparisons.dat", "w") as f:
    f.write("n qssorted qsrandom qsplus merge heap bound\n")
    for r in rows:
        f.write(" ".join(r) + "\n")
