"""Write the chart's data: comparisons of the two sorts against the number of items.

The counts come from the chapter's own functions, in listings/.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))

from count_comparisons import mixed  # noqa: E402
from insertion_sort import insertion_sort  # noqa: E402
from selection_sort import selection_sort  # noqa: E402

rows = ["n selection insreversed insmixed inssorted"]
for n in range(10, 201, 10):
    rows.append(
        f"{n} {selection_sort(list(range(n)))} "
        f"{insertion_sort(list(range(n, 0, -1)))} "
        f"{insertion_sort(mixed(n))} {insertion_sort(list(range(n)))}"
    )
(HERE / "out").mkdir(exist_ok=True)
(HERE / "out" / "comparisons.dat").write_text("\n".join(rows) + "\n")
