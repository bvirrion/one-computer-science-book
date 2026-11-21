"""measure.py: the chart's data from the measured output (outputs/timing.txt): total
time after q queries, by scanning and with the index (build included).

Run it again after every new capture of timing.txt; tests/test_measure_figure.py
fails while measure.dat and timing.txt disagree."""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMING = HERE.parent / "outputs" / "timing.txt"


def table(text):
    """The rows of measure.dat for the printed output text."""
    build = float(re.search(r"built in ([\d.]+) ms", text).group(1))
    per_query = re.search(r"([\d.]+) ms scanning the files, ([\d.]+) ms", text)
    scan, index = map(float, per_query.groups())
    rows = ["q scan index\n"]
    for q in range(11):
        rows.append(f"{q} {q * scan:.3f} {build + q * index:.3f}\n")
    return "".join(rows)


if __name__ == "__main__":
    (HERE / "measure.dat").write_text(table(TIMING.read_text()))
