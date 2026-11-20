"""Write vector_vs_list.dat from the output of listings/vector_vs_list.cpp."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "vector_vs_list.txt"
DAT = HERE / "vector_vs_list.dat"


def table(text: str) -> list[tuple[int, float, float]]:
    rows = []
    for line in text.splitlines()[2:]:             # the command, then the header
        n, vec, lst, _ = line.split()
        rows.append((int(n), float(vec), float(lst)))
    return rows


def main() -> None:
    rows = table(OUTPUT.read_text())
    DAT.write_text("n vector list\n" + "".join(f"{n} {v} {s}\n" for n, v, s in rows))


if __name__ == "__main__":
    main()
