"""Write aloha.dat from the output of listings/aloha_sim.py."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "aloha_sim.txt"
DAT = HERE / "aloha.dat"


def table(text):
    rows = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[0][0].isdigit():
            rows.append(tuple(float(p) for p in parts))
    return rows


def main():
    lines = "".join(f"{g} {s} {t}\n" for g, s, t in table(OUTPUT.read_text()))
    DAT.write_text("G simulated theory\n" + lines)


if __name__ == "__main__":
    main()
