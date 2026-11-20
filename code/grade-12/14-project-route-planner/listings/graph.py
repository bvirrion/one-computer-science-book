"""Milestone 2: a directed graph whose arcs carry a cost, read from the database."""
from collections import deque


def travel_seconds(length_m, speed_kmh):
    """Time to drive a road at its speed limit, rounded to the second."""
    return round(length_m * 3.6 / speed_kmh)     # km/h to m/s: divide by 3.6


class Graph:
    def __init__(self):
        self.arcs = {}                           # vertex -> {successor: cost}

    def add_vertex(self, v):
        self.arcs.setdefault(v, {})

    def add_arc(self, u, v, cost):
        self.add_vertex(u)
        self.add_vertex(v)
        self.arcs[u][v] = cost

    def successors(self, u):
        return self.arcs[u].items()

    def arc_count(self):
        return sum(len(s) for s in self.arcs.values())

    def reachable(self, start):
        seen, queue = {start}, deque([start])
        while queue:
            for v in self.arcs[queue.popleft()]:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
        return seen

    def one_way_arcs(self):
        return [(u, v) for u in self.arcs for v in self.arcs[u]
                if u not in self.arcs[v]]


def from_database(conn, criterion="time", closed=()):
    """Arcs from the roads; a one-way road gives one arc, the others two."""
    g = Graph()
    for (p,) in conn.execute("SELECT place_id FROM place"):
        g.add_vertex(p)
    for road, a, b, length, speed, one_way in conn.execute("SELECT * FROM road"):
        if road in closed:
            continue
        cost = travel_seconds(length, speed) if criterion == "time" else length
        g.add_arc(a, b, cost)
        if not one_way:
            g.add_arc(b, a, cost)
    return g
