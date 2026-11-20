"""Write koch_points.dat: the Koch curve at depth 3."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from koch import curve  # noqa: E402

with open(Path(__file__).with_suffix(".dat"), "w") as out:
    out.write("x y\n")
    for x, y in curve(3):
        out.write(f"{x:.5f} {y:.5f}\n")
