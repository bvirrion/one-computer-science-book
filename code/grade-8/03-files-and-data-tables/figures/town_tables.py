"""Copy the town tables read here into listings/; write the monthly chart's data.

    python code/grade-8/03-files-and-data-tables/figures/town_tables.py

tests/test_town_copy.py checks that the copies are byte for byte those of data/town/.
"""

import csv
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOWN = HERE.parents[3] / "data" / "town"
TABLES = ["books.csv", "loans.csv", "weather.csv"]


def monthly_means():
    """Mean temperature per month at Hilltop, without empty values and -99.0 codes."""
    sums = [0.0] * 12
    counts = [0] * 12
    with open(TOWN / "weather.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["station"] == "Hilltop" and row["temp_c"] not in ("", "-99.0"):
                month = int(row["date"][5:7]) - 1
                sums[month] += float(row["temp_c"])
                counts[month] += 1
    return [round(sums[m] / counts[m], 2) for m in range(12)]


def main():
    for name in TABLES:
        shutil.copyfile(TOWN / name, HERE.parent / "listings" / name)
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    rows = [f"{m + 1} {t}" for m, t in enumerate(monthly_means())]
    (out / "hilltop_monthly.dat").write_text("month temp\n" + "\n".join(rows) + "\n")
    print("copied", ", ".join(TABLES), "and wrote", out / "hilltop_monthly.dat")


if __name__ == "__main__":
    main()
