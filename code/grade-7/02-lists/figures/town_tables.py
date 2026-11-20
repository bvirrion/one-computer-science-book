"""Write the Hilltop rainfall lists of grade 7, chapter 2, from data/town/weather.csv.

    python code/grade-7/02-lists/figures/town_tables.py

listings/rain.py gets January as a list literal, listings/hilltop_2025.py the whole
year, figures/out/january.dat the bar chart. tests/test_lists.py checks both lists
against the CSV.
"""

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
LISTINGS = HERE.parent / "listings"


def hilltop_rain():
    with open(ROOT / "data" / "town" / "weather.csv", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["station"] == "Hilltop"]
    return [(r["date"], float(r["rain_mm"])) for r in rows]


def literal(values, indent="    ", per_line=10):
    lines = []
    for i in range(0, len(values), per_line):
        row = ", ".join(f"{v:.1f}" for v in values[i:i + per_line])
        lines.append(indent + row + ",")
    return "\n".join(lines)


def main():
    year = hilltop_rain()
    january = [v for d, v in year if d.startswith("2025-01")]
    rain_py = LISTINGS / "rain.py"
    body = rain_py.read_text().split("]\n", 1)[1]
    rain_py.write_text(
        "# Rainfall at Hilltop, January 2025, in millimetres (day 1 first).\n"
        "rain = [\n" + literal(january) + "\n]\n" + body
    )
    (LISTINGS / "hilltop_2025.py").write_text(
        '"""Daily rainfall at Hilltop in 2025, in millimetres, from 1 January."""\n\n'
        "month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]\n"
        "rain = [\n" + literal([v for _, v in year]) + "\n]\n"
    )
    (HERE.parent / "exercises" / "rain.py").write_bytes(rain_py.read_bytes())
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    (out / "january.dat").write_text(
        "day rain\n" + "".join(f"{i + 1} {v:.1f}\n" for i, v in enumerate(january))
    )
    print(f"January: {len(january)} days; year: {len(year)} days")


if __name__ == "__main__":
    main()
