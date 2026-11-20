"""Copy the town tables the explorer reads into listings/; write the genre chart's data.

    python code/grade-8/06-project-data-explorer/figures/town_tables.py

tests/test_town_copy.py checks that the copies are byte for byte those of data/town/.
The chart's counts come from the explorer's own function, loans_by_genre.
"""

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LISTINGS = HERE.parent / "listings"
TOWN = HERE.parents[3] / "data" / "town"

for name in ["books.csv", "loans.csv"]:
    shutil.copyfile(TOWN / name, LISTINGS / name)

sys.path.insert(0, str(LISTINGS))
from explorer_v5 import load_table, loans_by_genre  # noqa: E402

books = load_table(LISTINGS / "books.csv")
counts = loans_by_genre(books, load_table(LISTINGS / "loans.csv"))
rows = ["genre loans"]
for genre in sorted(counts):
    rows.append(f"{genre} {counts[genre]}")
(HERE / "out").mkdir(exist_ok=True)
(HERE / "out" / "genres.dat").write_text("\n".join(rows) + "\n")
