"""Write wa.dat (u, measured write amplification, 1/(1-u)) from the output of
listings/ftl.py, for the chart of the flash section."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "ftl.txt"


def table(text: str) -> list[tuple[float, float, float]]:
    rows = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 5 and parts[0].startswith("0."):
            rows.append((float(parts[0]), float(parts[1]), float(parts[4])))
    return rows


def main() -> None:
    body = "".join(f"{u} {wa} {bound}\n" for u, wa, bound in table(OUTPUT.read_text()))
    (HERE / "wa.dat").write_text("u wa average\n" + body)


if __name__ == "__main__":
    main()
