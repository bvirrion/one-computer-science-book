"""Write regions_k1.dat and regions_k7.dat: the class predicted on a grid (scaled)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from error_rate import scaled, train  # noqa: E402
from knn import predict  # noqa: E402

for k in (1, 7):
    with open(Path(__file__).parent / f"regions_k{k}.dat", "w") as out:
        out.write("thickness mass label\n")
        for i in range(41):
            for j in range(41):
                x = (2.0 * i, 30.0 * j, "?")       # 0..80 mm, 0..1200 g
                out.write(f"{x[0]} {x[1]} {predict(train, x, k, scaled)}\n")
