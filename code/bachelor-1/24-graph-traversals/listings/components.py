"""components.py: the connected components of an undirected graph."""

from graph import friendships


def components(g):
    """The components, each a sorted list of vertices; one search per component."""
    seen, out = set(), []
    for s in g.vertices():
        if s in seen:
            continue
        seen.add(s)
        stack, comp = [s], []
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in g.adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        out.append(sorted(comp))
    return out


if __name__ == "__main__":
    for c in components(friendships()):
        print(f"{len(c):2} people:", c if len(c) < 15 else f"{c[:6]} ... {c[-3:]}")
