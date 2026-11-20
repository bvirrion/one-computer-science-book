"""graph.py: graphs as adjacency lists, and the town's roads and friendships."""

import csv
from dataclasses import dataclass, field
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


@dataclass
class Graph:
    directed: bool
    adj: dict = field(default_factory=dict)  # vertex -> list of neighbours

    def add_vertex(self, v):
        self.adj.setdefault(v, [])

    def add_edge(self, u, v):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)  # an undirected edge is stored at both ends

    def vertices(self):
        return list(self.adj)

    def edges(self):
        """Each edge once: (u, v) with u before v in an undirected graph."""
        order = {v: i for i, v in enumerate(self.adj)}
        return [(u, v) for u in self.adj for v in self.adj[u]
                if self.directed or order[u] < order[v] or u == v]

    def reversed(self):
        r = Graph(self.directed)
        for v in self.adj:
            r.add_vertex(v)
        for u, v in self.edges():
            r.add_edge(v, u)
        return r


def rows(name):
    with open(TOWN / f"{name}.csv", newline="") as f:
        return list(csv.DictReader(f))


def roads():
    """Places joined by roads; a one-way road is an arc, any other road two arcs."""
    g = Graph(directed=True)
    for p in rows("places"):
        g.add_vertex(int(p["place_id"]))
    for r in rows("roads"):
        a, b = int(r["from_place"]), int(r["to_place"])
        g.add_edge(a, b)
        if r["one_way"] == "0":
            g.add_edge(b, a)
    return g


def friendships():
    """People 1 to 40, joined when they are friends."""
    g = Graph(directed=False)
    for v in range(1, 41):
        g.add_vertex(v)
    for r in rows("friendships"):
        g.add_edge(int(r["person_a"]), int(r["person_b"]))
    return g


def place_names():
    return {int(p["place_id"]): p["name"] for p in rows("places")}


if __name__ == "__main__":
    for name, g in (("roads", roads()), ("friendships", friendships())):
        degrees = [len(g.adj[v]) for v in g.vertices()]
        print(f"{name}: {len(g.vertices())} vertices, {len(g.edges())} edges"
              f" ({'arcs' if g.directed else 'undirected'}),"
              f" {'out-' if g.directed else ''}degrees {min(degrees)}"
              f" to {max(degrees)},"
              f" sum {sum(degrees)}")
