from db import build
from graph import from_database, travel_seconds

conn = build()
g = from_database(conn)
print(len(g.arcs), "vertices,", g.arc_count(), "arcs")
print("road 2:", travel_seconds(1210, 50), "s for 1210 m at 50 km/h")
everyone = set(g.arcs)
print("every place reaches every place:",
      all(g.reachable(p) == everyone for p in g.arcs))
print("arcs without their reverse:", g.one_way_arcs())
print("from the Station (2):", dict(g.successors(2)))
