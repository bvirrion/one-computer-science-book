"""Milestone 5: every pair of places, the slowest one, and a road closed."""
from graph import from_database
from planner import RoutePlanner, dijkstra, rebuild

planner = RoutePlanner()
g = from_database(planner.conn)
times = {}
for a in g.arcs:                                 # one Dijkstra per starting place
    dist, _ = dijkstra(g, a)
    times.update({(a, b): t for b, t in dist.items() if b != a})
print(len(times), "ordered pairs; mean", round(sum(times.values()) / len(times)), "s")
a, b = max(times, key=times.get)
path = rebuild(dijkstra(g, a)[1], b)
print(f"slowest: {planner.names[a]} to {planner.names[b]}, {times[a, b]} s,"
      f" {len(path) - 1} roads")
names = [planner.names[p] for p in path]
print("  " + " > ".join(names[:6]) + " >")
print("  " + " > ".join(names[6:]))

for road in [2, 6]:
    planner.close_road(road)
    path, seconds = planner.route("Station", "Library")
    print(f"road {road} closed: {seconds} s, {len(path) - 1} roads")
    print("  " + " > ".join(path))
    planner.reopen_road(road)
