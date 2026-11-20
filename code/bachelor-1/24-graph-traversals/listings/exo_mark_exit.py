"""exo_mark_exit.py: exercise 5, a search that marks a vertex when it leaves it."""

from graph import Graph

visits = 0


def search(g, u, done):
    global visits
    visits += 1
    for v in g.adj[u]:
        if v not in done:
            search(g, v, done)
    done.add(u)  # marked on exit only


def ladder(k):
    """k diamonds in a row: from each joint, two ways to the next joint."""
    g = Graph(directed=True)
    for i in range(k):
        g.add_edge(f"j{i}", f"a{i}"), g.add_edge(f"j{i}", f"b{i}")
        g.add_edge(f"a{i}", f"j{i + 1}"), g.add_edge(f"b{i}", f"j{i + 1}")
    return g


if __name__ == "__main__":
    g = ladder(10)
    search(g, "j0", set())
    print(f"10 diamonds, no cycle: {len(g.vertices())} vertices, {visits} visits")
    g = Graph(directed=True)
    g.add_edge("x", "y"), g.add_edge("y", "x")
    try:
        search(g, "x", set())
    except RecursionError:
        print("a cycle x -> y -> x: RecursionError")
