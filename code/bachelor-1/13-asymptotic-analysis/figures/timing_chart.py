"""timing_chart.py: nanoseconds per counted comparison, from the captured outputs
of doubling.py (counts) and timing.py (times measured on the author's laptop)."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"


def rows(name):
    lines = (OUT / name).read_text().splitlines()[2:]
    return [line.split()[:4] for line in lines]


with open(HERE / "timing.dat", "w") as f:
    f.write("n max merge ins\n")
    for counts, times in zip(rows("doubling.txt"), rows("timing.txt")):
        n = int(counts[0])
        ns = [1e6 * float(t) / int(c) for c, t in zip(counts[1:], times[1:])]
        f.write(f"{n} {ns[0]:.2f} {ns[1]:.2f} {ns[2]:.2f}\n")
