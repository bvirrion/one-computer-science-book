"""Write kmp_bench.dat from the measured output of kmp_bench.c."""
from pathlib import Path

HERE = Path(__file__).parent
DAT = HERE / "kmp_bench.dat"


def main():
    rows = (HERE.parent / "outputs" / "kmp_bench.txt").read_text().splitlines()[2:]
    data = [r.split() for r in rows if r.split()]
    DAT.write_text("n naive kmp\n" + "".join(f"{r[0]} {r[2]} {r[4]}\n" for r in data))


if __name__ == "__main__":
    main()
