"""Write index_timing.dat from the captured output of index_timing.py."""
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent / "outputs" / "index_timing.txt"
DAT = HERE / "index_timing.dat"


def main():
    rows = [line.split()[:3] for line in SRC.read_text().splitlines()[2:]]
    DAT.write_text("rows scan index\n" + "".join(" ".join(r) + "\n" for r in rows))
    return rows


if __name__ == "__main__":
    main()
