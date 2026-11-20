"""Exercises of the route-planner project."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from graph import Graph, travel_seconds  # noqa: E402
from planner import RoutePlanner, dijkstra, rebuild  # noqa: E402


def place_id(conn, name):                                    # exercise 5
    row = conn.execute("SELECT place_id FROM place WHERE name = ?", (name,)).fetchone()
    if row is None:
        raise ValueError(f"no place called {name!r}")
    return row[0]


def graph_both_ways(conn):                                   # exercise 6: the fault
    g = Graph()
    for _, a, b, length, speed, _ in conn.execute("SELECT * FROM road"):
        g.add_arc(a, b, travel_seconds(length, speed))
        g.add_arc(b, a, travel_seconds(length, speed))       # one_way forgotten
    return g


def graph_by_roads(conn):                                    # exercise 7
    """Every road costs 1: the route with the fewest roads."""
    g = Graph()
    for _, a, b, _, _, one_way in conn.execute("SELECT * FROM road"):
        g.add_arc(a, b, 1)
        if not one_way:
            g.add_arc(b, a, 1)
    return g


def roads_on_route(conn, ids):                               # exercise 10
    found = []
    for a, b in zip(ids, ids[1:]):
        (road,) = conn.execute("SELECT road_id FROM road WHERE (from_place, to_place)"
                               " IN ((?, ?), (?, ?))", (a, b, b, a)).fetchone()
        found.append(road)
    return found


def route_avoiding(planner, start, end, avoid):              # exercise 12
    from graph import from_database
    g = from_database(planner.conn, "time", planner.closed)
    banned = planner.place_id(avoid)
    for succ in g.arcs.values():
        succ.pop(banned, None)
    del g.arcs[banned]
    a, b = planner.place_id(start), planner.place_id(end)
    dist, parent = dijkstra(g, a)
    return [planner.names[p] for p in rebuild(parent, b)], dist[b]


def within(planner, start, seconds):                         # exercise 14
    from graph import from_database
    dist, _ = dijkstra(from_database(planner.conn), planner.place_id(start))
    return sorted(planner.names[p] for p, t in dist.items() if 0 < t <= seconds)


if __name__ == "__main__":
    p = RoutePlanner()
    print(p.route("Bakery Corner", "South School"))
    print(travel_seconds(1830, 30))
    print(p.conn.execute("SELECT COUNT(*), MAX(length_m) FROM road"
                         " WHERE speed_kmh = 30").fetchall())
    g = graph_both_ways(p.conn)
    print(dijkstra(g, 3)[0][1], g.arc_count())
    gr = graph_by_roads(p.conn)
    d, par = dijkstra(gr, p.place_id("Old Mill"))
    print(d[p.place_id("Post Office")], [p.names[x] for x in rebuild(par, 18)])
    path, _ = p.route("Station", "Library")
    print(roads_on_route(p.conn, [p.place_id(n) for n in path]))
    print(route_avoiding(p, "Station", "Library", "North Bridge"))
    print(within(p, "Station", 120))
