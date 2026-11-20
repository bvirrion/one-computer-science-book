"""Write cpi.dat from the output of cpi_table.py (captured in run_branches.txt)."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "run_branches.txt"
DAT = HERE / "cpi.dat"


def table(text):
    lines = text.splitlines()
    start = lines.index("$ python cpi_table.py") + 2
    rows = []
    for line in lines[start:start + 3]:
        name, _, a, b, c = line.split()
        key = name.removesuffix(".S").replace("_", "-")
        rows.append((key, float(a), float(b), float(c)))
    return rows


def main():
    rows = table(OUTPUT.read_text())
    body = "".join(f"{n} {a} {b} {c}\n" for n, a, b, c in rows)
    DAT.write_text("program nofwd fwd fwdpred\n" + body)


if __name__ == "__main__":
    main()
