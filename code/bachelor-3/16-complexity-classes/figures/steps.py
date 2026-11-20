"""Write steps.dat (n, sums computed by the search, steps of a check) from the output of
listings/search_vs_verify.py, for the chart of the section on P and NP."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "search_vs_verify.txt"


def table(text: str) -> list[tuple[int, int, int]]:
    rows = []
    for line in text.splitlines():
        parts = line.replace(",", "").split()
        if len(parts) == 3 and parts[0].isdigit():
            rows.append((int(parts[0]), int(parts[1]), int(parts[2])))
    return rows


def main() -> None:
    rows = table(OUTPUT.read_text())
    body = "".join(f"{n} {search} {verify}\n" for n, search, verify in rows)
    (HERE / "steps.dat").write_text("n search verify\n" + body)


if __name__ == "__main__":
    main()
