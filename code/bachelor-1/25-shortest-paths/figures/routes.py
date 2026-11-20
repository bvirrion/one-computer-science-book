"""routes.py: the .dat files of the map: roads, the fastest and the shortest route from
the Town Square to the Hospital."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))
from dijkstra import dijkstra, path  # noqa: E402
from wgraph import roads, rows  # noqa: E402

xy = {int(p["place_id"]): (int(p["x_m"]) / 1000, int(p["y_m"]) / 1000)
      for p in rows("places")}
with open(HERE / "roads.dat", "w") as out:
    out.write("x y\n")
    for r in rows("roads"):
        for p in (int(r["from_place"]), int(r["to_place"])):
            out.write("{} {}\n".format(*xy[p]))
        out.write("\n")
for name, weight in (("fast", "seconds"), ("short", "metres")):
    route = path(dijkstra(roads(weight), 1)[1], 8)
    with open(HERE / f"{name}.dat", "w") as out:
        out.write("x y\n" + "".join("{} {}\n".format(*xy[p]) for p in route))
with open(HERE / "places.dat", "w") as out:
    out.write("x y\n" + "".join("{} {}\n".format(*xy[p]) for p in sorted(xy)))
