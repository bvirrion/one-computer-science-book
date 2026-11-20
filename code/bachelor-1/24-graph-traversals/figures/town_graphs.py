"""town_graphs.py: the .dat files of the road map (places at their coordinates, each
with its number of roads from the Town Square) and of the friendship graph (the three
groups on three circles, bridges apart)."""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))
from bfs import bfs  # noqa: E402
from bridges import bridges  # noqa: E402
from graph import friendships, roads, rows  # noqa: E402

places = {int(p["place_id"]): (int(p["x_m"]) / 1000, int(p["y_m"]) / 1000)
          for p in rows("places")}
dist, _ = bfs(roads(), 1)
with open(HERE / "roads.dat", "w") as out:
    out.write("x y\n")
    for r in rows("roads"):
        if r["one_way"] == "0":
            for p in (int(r["from_place"]), int(r["to_place"])):
                out.write("{} {}\n".format(*places[p]))
            out.write("\n")
with open(HERE / "oneway.dat", "w") as out:
    r = rows("roads")[0]
    out.write("x y\n" + "".join("{} {}\n".format(*places[int(r[k])])
                                for k in ("from_place", "to_place")))
with open(HERE / "places.dat", "w") as out:
    out.write("x y d id\n")
    for p, (x, y) in places.items():
        out.write(f"{x} {y} {dist[p]} {p}\n")

g = friendships()
centres = {0: (0.0, 0.0), 1: (7.0, 0.0), 2: (3.5, -5.8)}
groups = {0: range(1, 15), 1: range(15, 28), 2: range(28, 40)}
pos = {40: (7.5, -5.2)}
for k, members in groups.items():
    cx, cy = centres[k]
    order, seen = [], set()  # around the circle in depth-first order, fewer crossings
    for s in members:
        stack = [s]
        while stack:
            u = stack.pop()
            if u not in seen:
                seen.add(u)
                order.append(u)
                stack += [w for w in sorted(g.adj[u], reverse=True) if w in members]
    members = order
    for i, v in enumerate(members):
        a = 2 * math.pi * i / len(members)
        pos[v] = (round(cx + 2.5 * math.cos(a), 3), round(cy + 2.5 * math.sin(a), 3))
cut = {frozenset(e) for e in bridges(g)}
with open(HERE / "friend_edges.dat", "w") as plain, \
        open(HERE / "friend_bridges.dat", "w") as bold:
    plain.write("x y\n")
    bold.write("x y\n")
    for u, v in g.edges():
        out = bold if frozenset((u, v)) in cut else plain
        out.write("{} {}\n{} {}\n\n".format(*pos[u], *pos[v]))
with open(HERE / "people.dat", "w") as out:
    out.write("x y id\n")
    out.write("".join(f"{x} {y} {v}\n" for v, (x, y) in sorted(pos.items())))
