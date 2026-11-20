"""Write copy_times.dat from the output of listings/buffered_vs_raw.c."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "buffered_vs_raw.txt"
DAT = HERE / "copy_times.dat"


def table(text):
    rows = []
    for line in text.splitlines()[2:]:
        if not line.startswith("putc"):
            b, reads, ms = line.split()
            rows.append((int(b), int(reads), float(ms)))
    return rows


def main():
    rows = table(OUTPUT.read_text())
    DAT.write_text("b reads ms\n" + "".join(f"{b} {x} {t}\n" for b, x, t in rows))


if __name__ == "__main__":
    main()
