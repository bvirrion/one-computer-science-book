"""Write lost.dat from the output of listings/race.c (one measured run)."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "race.txt"
DAT = HERE / "lost.dat"


def table(text):
    rows = []
    for line in text.splitlines()[2:]:
        f = line.split()
        rows.append((int(f[0]), int(f[1]), int(f[2]), float(f[3])))
    return rows


def main():
    rows = table(OUTPUT.read_text())
    DAT.write_text("threads expected got lost\n"
                   + "".join(f"{k} {e} {g} {p}\n" for k, e, g, p in rows))


if __name__ == "__main__":
    main()
