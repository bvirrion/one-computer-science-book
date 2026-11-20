"""Write map_roads.dat, map_route.dat and map_places.dat: the town's roads, and the
slowest of the fastest routes (Old Mill to Post Office) as the planner finds it."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "listings"))
import town  # noqa: E402
from planner import RoutePlanner  # noqa: E402

xy = {p["place_id"]: f'{p["x_m"] / 1000:.3f} {p["y_m"] / 1000:.3f}'
      for p in town.load("places")}
planner = RoutePlanner()
path, _ = planner.route("Old Mill", "Post Office")
ids = [planner.place_id(name) for name in path]
with open(HERE / "map_roads.dat", "w") as out:
    out.write("x y\n" + "".join(f"{xy[r['from_place']]}\n{xy[r['to_place']]}\n\n"
                                for r in town.load("roads")))
with open(HERE / "map_route.dat", "w") as out:
    out.write("x y\n" + "".join(f"{xy[p]}\n" for p in ids))
with open(HERE / "map_places.dat", "w") as out:
    out.write("x y id\n" + "".join(f"{xy[p]} {p}\n" for p in sorted(xy)))
