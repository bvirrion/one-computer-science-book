"""Write count.dat (A's and B's distance to C per round) from the printed output."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "distance_vector.txt"
DAT = HERE / "count.dat"


def table(text):
    rows = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 10 and parts[0] == "round" and parts[2] == "A":
            rows.append((int(parts[1]), int(parts[3]), int(parts[7])))
    return rows


def main():
    rows = "".join(f"{r} {a} {b}\n" for r, a, b in table(OUTPUT.read_text()))
    DAT.write_text("round A B\n" + rows)


if __name__ == "__main__":
    main()
