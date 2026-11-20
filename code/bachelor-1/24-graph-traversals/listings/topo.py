"""topo.py: a topological order of a directed acyclic graph, by depth-first search
and by removing vertices without incoming arcs (Kahn)."""

from collections import deque

from graph import Graph

PREREQUISITES = [  # (before, after): chapters of this book that rely on one another
    ("types", "functions"), ("functions", "pointers"), ("pointers", "memory"),
    ("memory", "lists"), ("pointers", "arrays"), ("induction", "correctness"),
    ("correctness", "complexity"), ("complexity", "sorting"), ("arrays", "hashing"),
    ("lists", "hashing"), ("complexity", "hashing"), ("sorting", "graphs"),
    ("hashing", "graphs"),
]


def by_dfs(g):
    """Vertices by decreasing finishing time."""
    done, order = set(), []

    def visit(u):
        done.add(u)
        for v in g.adj[u]:
            if v not in done:
                visit(v)
        order.append(u)  # u finishes after everything reachable from it

    for s in g.vertices():
        if s not in done:
            visit(s)
    return order[::-1]


def by_kahn(g):
    indegree = {v: 0 for v in g.vertices()}
    for _, v in g.edges():
        indegree[v] += 1
    ready = deque(v for v in g.vertices() if indegree[v] == 0)
    order = []
    while ready:
        u = ready.popleft()
        order.append(u)
        for v in g.adj[u]:  # removing u: its successors lose an incoming arc
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)
    return order if len(order) == len(indegree) else None  # None: a cycle remains


def is_topological(g, order):
    position = {v: i for i, v in enumerate(order)}
    return all(position[u] < position[v] for u, v in g.edges())


if __name__ == "__main__":
    g = Graph(directed=True)
    for u, v in PREREQUISITES:
        g.add_edge(u, v)
    for name, order in (("depth-first", by_dfs(g)), ("Kahn", by_kahn(g))):
        print(f"{name}, topological: {is_topological(g, order)}")
        print("  " + " ".join(order[:6]) + "\n  " + " ".join(order[6:]))
