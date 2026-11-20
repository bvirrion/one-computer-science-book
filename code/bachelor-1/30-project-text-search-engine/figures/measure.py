"""measure.py: the chart's data from the measured output (outputs/timing.txt): total
time after q queries, by scanning and with the index (build included)."""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
text = (HERE.parent / "outputs" / "timing.txt").read_text()
build = float(re.search(r"built in ([\d.]+) ms", text).group(1))
scan, index = map(float, re.search(r"([\d.]+) ms scanning the files, ([\d.]+) ms", text)
                  .groups())
with open(HERE / "measure.dat", "w") as f:
    f.write("q scan index\n")
    for q in range(11):
        f.write(f"{q} {q * scan:.3f} {build + q * index:.3f}\n")
