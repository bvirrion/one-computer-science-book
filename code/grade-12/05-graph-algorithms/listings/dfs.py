from representations import G


def dfs_stack(g, start):
    """Depth-first order with an explicit stack."""
    order, visited, stack = [], set(), [start]
    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        order.append(v)
        for w in reversed(g[v]):            # reversed: the first neighbour on top
            if w not in visited:
                stack.append(w)
    return order


def dfs_rec(g, v, visited=None):
    """The same order, with the call stack of the recursion."""
    if visited is None:
        visited = []
    visited.append(v)
    for w in g[v]:
        if w not in visited:
            dfs_rec(g, w, visited)
    return visited


if __name__ == "__main__":
    print("with a stack:   ", dfs_stack(G, "A"))
    print("with recursion: ", dfs_rec(G, "A"))
    print("reachable from E:", sorted(dfs_stack(G, "E")))
