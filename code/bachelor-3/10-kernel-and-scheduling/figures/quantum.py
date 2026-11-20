"""Write quantum.dat (q, average turnaround, average response) from the output of
listings/rr_quantum.py, for the chart of the weekend problem."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "rr_quantum.txt"


def table(text: str) -> list[tuple[int, float, float]]:
    rows = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 7 and parts[0].isdigit():
            rows.append((int(parts[0]), float(parts[1]), float(parts[2])))
    return rows


def main() -> None:
    rows = table(OUTPUT.read_text())
    body = "".join(f"{q} {turn} {resp}\n" for q, turn, resp in rows)
    (HERE / "quantum.dat").write_text("q turnaround response\n" + body)


if __name__ == "__main__":
    main()
