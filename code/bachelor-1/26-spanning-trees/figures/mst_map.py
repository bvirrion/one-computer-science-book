"""mst_map.py: the .dat files of the map: the roads, Kruskal's forest after 15 roads,
and the whole minimum spanning tree."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))
from kruskal import kruskal  # noqa: E402
from mst_town import rows, town  # noqa: E402

xy = {int(p["place_id"]): (int(p["x_m"]) / 1000, int(p["y_m"]) / 1000)
      for p in rows("places")}
vertices, edges = town()
tree, _ = kruskal(vertices, edges)


def segments(name, chosen):
    with open(HERE / name, "w") as out:
        out.write("x y\n")
        for _, u, v in chosen:
            out.write("{} {}\n{} {}\n\n".format(*xy[u], *xy[v]))


segments("roads.dat", edges)
segments("forest.dat", tree[:15])
segments("mst.dat", tree)
with open(HERE / "places.dat", "w") as out:
    out.write("x y\n" + "".join("{} {}\n".format(*xy[p]) for p in sorted(xy)))
