"""Write monthly_means.dat: monthly means, Riverside raw and clean, Hilltop clean."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "exercises"))
from corrected_weather import PATH, clean, monthly  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from load_weather import read_table  # noqa: E402

OUT = Path(__file__).with_suffix(".dat")


def main():
    rows = read_table(PATH)
    good = clean(rows)
    raw_r = monthly(rows, "Riverside")
    clean_r = monthly(good, "Riverside")
    clean_h = monthly(good, "Hilltop")
    lines = ["month riverside_raw riverside hilltop"]
    for m in sorted(clean_r):
        lines.append(f"{int(m)} {raw_r[m]:.3f} {clean_r[m]:.3f} {clean_h[m]:.3f}")
    OUT.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
