"""Write eight_puzzle.dat from the captured output of eight_puzzle.py."""
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent / "outputs" / "eight_puzzle.txt"
DAT = HERE / "eight_puzzle.dat"


def main():
    rows = [line.split() for line in SRC.read_text().splitlines()[2:]]
    DAT.write_text("depth bfs misplaced manhattan\n"
                   + "".join(" ".join(r) + "\n" for r in rows))
    return rows


if __name__ == "__main__":
    main()
