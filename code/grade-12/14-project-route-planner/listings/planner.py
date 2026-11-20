"""Milestones 3 and 4: shortest routes, and the planner that the interface uses."""
from db import build
from graph import from_database


def dijkstra(g, source):
    """Smallest cost from source to every vertex, and each vertex's parent."""
    dist, parent, done = {source: 0}, {source: None}, set()
    while len(done) < len(dist):
        u = min((v for v in dist if v not in done), key=dist.get)
        done.add(u)                              # dist[u] is now final
        for v, cost in g.successors(u):
            if v not in done and (v not in dist or dist[u] + cost < dist[v]):
                dist[v], parent[v] = dist[u] + cost, u
    return dist, parent


def rebuild(parent, target):
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]


class RoutePlanner:
    """Routes between the places of the town, by time (seconds) or by distance (m)."""

    def __init__(self, conn=None):
        self.conn = conn or build()
        self.names = dict(self.conn.execute("SELECT place_id, name FROM place"))
        self.ids = {name: p for p, name in self.names.items()}
        self.closed = set()

    def place_id(self, name):
        if name not in self.ids:
            raise ValueError(f"no place called {name!r}")
        return self.ids[name]

    def route(self, start, end, criterion="time"):
        """The best route as a list of names, and its total cost."""
        g = from_database(self.conn, criterion, self.closed)
        a, b = self.place_id(start), self.place_id(end)
        dist, parent = dijkstra(g, a)
        if b not in dist:
            raise ValueError(f"{end!r} cannot be reached from {start!r}")
        return [self.names[p] for p in rebuild(parent, b)], dist[b]

    def cost_of(self, path, criterion="time"):
        """The cost of a given route, as a list of names, by either criterion."""
        g = from_database(self.conn, criterion, self.closed)
        ids = [self.place_id(name) for name in path]
        return sum(g.arcs[a][b] for a, b in zip(ids, ids[1:]))

    def close_road(self, road_id):
        self.closed.add(road_id)

    def reopen_road(self, road_id):
        self.closed.discard(road_id)
