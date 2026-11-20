"""Write parcels_plot.dat: the training set, one row per item."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from parcels import make_items, split  # noqa: E402

train, _, _ = split(make_items())
with open(Path(__file__).with_suffix(".dat"), "w") as out:
    out.write("thickness mass label\n")
    for t, m, label in train:
        out.write(f"{t} {m} {label}\n")
