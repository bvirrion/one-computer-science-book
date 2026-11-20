"""dfs.py: depth-first search with discovery and finishing times, and the class of every
arc of a directed graph."""

from graph import Graph


def dfs(g):
    """(discovery, finish, parent, classes): times run 1, 2, ...; classes maps each arc
    to 'tree', 'back', 'forward' or 'cross'."""
    disc, fin, parent, classes = {}, {}, {}, {}
    clock = 0

    def visit(u):
        nonlocal clock
        clock += 1
        disc[u] = clock  # u is now open: discovered, not finished
        for v in g.adj[u]:
            if v not in disc:
                classes[u, v] = "tree"
                parent[v] = u
                visit(v)
            elif v not in fin:
                classes[u, v] = "back"  # v is open: an ancestor of u
            elif disc[u] < disc[v]:
                classes[u, v] = "forward"  # v finished, a descendant of u
            else:
                classes[u, v] = "cross"
        clock += 1
        fin[u] = clock

    for s in g.vertices():
        if s not in disc:
            parent[s] = None
            visit(s)
    return disc, fin, parent, classes


def dfs_iterative(g, s):
    """The vertices reachable from s in the order a stack discovers them."""
    seen, order, stack = set(), [], [s]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        order.append(u)
        stack.extend(reversed(g.adj[u]))  # so that neighbours come off in list order
    return order


def example():
    g = Graph(directed=True)
    for u, v in ["ab", "ac", "bd", "da", "ad", "cb", "ef", "fg", "ge", "ec", "gh"]:
        g.add_edge(u, v)
    return g


def main():
    g = example()
    disc, fin, _, classes = dfs(g)
    print("  ".join(f"{v} {disc[v]}/{fin[v]}" for v in sorted(g.vertices())))
    for kind in ("tree", "back", "forward", "cross"):
        arcs = [u + v for (u, v), k in classes.items() if k == kind]
        print(f"{kind:8}", " ".join(arcs))
    print("iterative, from a:", " ".join(dfs_iterative(g, "a")))


if __name__ == "__main__":
    main()
