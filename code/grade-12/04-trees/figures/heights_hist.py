"""Write heights_hist.dat: how many of 1000 random orders give each height."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from random_heights import heights  # noqa: E402

counts = Counter(heights())
with open(Path(__file__).with_suffix(".dat"), "w") as out:
    out.write("height count\n")
    for h in range(min(counts), max(counts) + 1):
        out.write(f"{h} {counts[h]}\n")
