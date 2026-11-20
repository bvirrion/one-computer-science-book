"""Write backtrack.dat from the measured output of backtracking.py."""
from pathlib import Path

HERE = Path(__file__).parent
DAT = HERE / "backtrack.dat"


def main():
    rows = (HERE.parent / "outputs" / "backtracking.txt").read_text().splitlines()[2:]
    data = [r.split()[:2] for r in rows if r.split() and r.split()[1] != "over"]
    DAT.write_text("n seconds\n" + "".join(f"{n} {t}\n" for n, t in data))


if __name__ == "__main__":
    main()
