"""Write load.dat (in-process throughput) from the captured output of load.rs."""
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent / "outputs" / "load.txt"
DAT = HERE / "load.dat"


def main():
    lines = SRC.read_text().splitlines()
    start = lines.index("threads  one lock  16 shards") + 1
    rows = [line.split() for line in lines[start:start + 4]]
    DAT.write_text("threads one sharded\n" + "".join(" ".join(r) + "\n" for r in rows))
    return rows


if __name__ == "__main__":
    main()
