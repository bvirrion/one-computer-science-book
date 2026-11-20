"""Write town_roads.dat, town_tree.dat and town_places.dat: the shortest-route tree
from the Station over the town's roads."""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "listings"))
from dijkstra import dijkstra  # noqa: E402

with open(HERE.parent / "listings" / "places.csv", newline="") as f:
    places = {int(r["place_id"]): r for r in csv.DictReader(f)}
g = {p: {} for p in places}
roads = []
with open(HERE.parent / "listings" / "roads.csv", newline="") as f:
    for r in csv.DictReader(f):
        a, b, m = int(r["from_place"]), int(r["to_place"]), int(r["length_m"])
        g[a][b] = m
        if r["one_way"] == "0":
            g[b][a] = m
        roads.append((a, b))
dist, parent = dijkstra(g, 2)


def xy(p):
    return f'{int(places[p]["x_m"]) / 1000:.3f} {int(places[p]["y_m"]) / 1000:.3f}'


with open(HERE / "town_roads.dat", "w") as out:
    out.write("x y\n" + "".join(f"{xy(a)}\n{xy(b)}\n\n" for a, b in roads))
with open(HERE / "town_tree.dat", "w") as out:
    edges = [(parent[v], v) for v in g if parent[v]]
    out.write("x y\n" + "".join(f"{xy(a)}\n{xy(b)}\n\n" for a, b in edges))
with open(HERE / "town_places.dat", "w") as out:
    out.write("x y d\n" + "".join(f"{xy(p)} {dist[p] / 1000:.1f}\n" for p in places))
