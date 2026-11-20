"""charts.py: products.dat and times.dat for the charts, from the captured outputs."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"


def table(name, first):
    rows = []
    for line in (OUT / name).read_text().splitlines():
        cells = line.split()
        if cells and cells[0].isdigit() and int(cells[0]) >= first:
            rows.append(cells)
    return rows


with open(HERE / "products.dat", "w") as f:
    f.write("n school karatsuba\n")
    for n, school, kara, _ in table("karatsuba.txt", 2):
        f.write(f"{n} {school} {kara}\n")
with open(HERE / "times.dat", "w") as f:
    f.write("n school c1 c8 c32\n")
    for cells in table("karatsuba_timing.txt", 16):
        f.write(" ".join(cells) + "\n")
