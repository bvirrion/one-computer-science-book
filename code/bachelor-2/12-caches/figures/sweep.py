"""Write sweep.dat from the output of listings/sweep.c (one measured run)."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "sweep.txt"
DAT = HERE / "sweep.dat"


def table(text):
    rows = []
    for line in text.splitlines()[2:]:          # the command, then the header
        size, ns = line.split()
        rows.append((int(size), float(ns)))
    return rows


def main():
    rows = table(OUTPUT.read_text())
    DAT.write_text("kib ns\n" + "".join(f"{k} {ns}\n" for k, ns in rows))


if __name__ == "__main__":
    main()
