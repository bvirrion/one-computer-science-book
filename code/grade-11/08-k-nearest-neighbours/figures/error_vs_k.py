"""Write error_vs_k.dat: validation error for each k, unscaled and scaled (percent)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from distance import distance  # noqa: E402
from error_rate import error_rate, scaled, train, validation  # noqa: E402

with open(Path(__file__).with_suffix(".dat"), "w") as out:
    out.write("k unscaled scaled\n")
    for k in range(1, 16):
        raw = 100 * error_rate(train, validation, k, distance)
        sc = 100 * error_rate(train, validation, k, scaled)
        out.write(f"{k} {raw:.2f} {sc:.2f}\n")
