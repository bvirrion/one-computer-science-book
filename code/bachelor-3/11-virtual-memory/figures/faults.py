"""Write faults.dat (frames, then the faults of FIFO, LRU, clock and OPT) for Belady's
string, from the output of listings/replace.py."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "replace.txt"


def table(text: str) -> dict[str, list[int]]:
    rows: dict[str, list[int]] = {}
    for line in text.splitlines():
        parts = line.split()
        if parts and parts[0] == "a":  # the second string starts: stop
            break
        if len(parts) == 6 and parts[0] in ("FIFO", "LRU", "clock", "OPT"):
            rows[parts[0]] = [int(x) for x in parts[1:]]
    return rows


def main() -> None:
    rows = table(OUTPUT.read_text())
    body = "".join(f"{f} " + " ".join(str(rows[k][f - 1]) for k in rows) + "\n"
                   for f in range(1, 6))
    (HERE / "faults.dat").write_text("frames " + " ".join(rows) + "\n" + body)


if __name__ == "__main__":
    main()
