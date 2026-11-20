"""kosaraju.py: the strongly connected components of a directed graph, two searches."""

from graph import Graph, roads, rows


def finishing_order(g):
    done, order = set(), []
    for s in g.vertices():
        if s in done:
            continue
        done.add(s)
        stack = [(s, iter(g.adj[s]))]  # iterative DFS: a vertex and its unexplored arcs
        while stack:
            u, arcs = stack[-1]
            for v in arcs:
                if v not in done:
                    done.add(v)
                    stack.append((v, iter(g.adj[v])))
                    break
            else:  # no arc left: u finishes
                stack.pop()
                order.append(u)
    return order


def kosaraju(g):
    """Components as lists; the first search orders, the second, on the reversed graph,
    collects. Components come out in a topological order of the component graph."""
    r, comps, assigned = g.reversed(), [], set()
    for s in reversed(finishing_order(g)):  # by decreasing finishing time
        if s in assigned:
            continue
        assigned.add(s)
        comp, stack = [], [s]
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in r.adj[u]:
                if v not in assigned:
                    assigned.add(v)
                    stack.append(v)
        comps.append(sorted(comp))
    return comps


def small():
    g = Graph(directed=True)
    for u, v in ["ab", "bc", "ca", "bd", "de", "ed", "cf", "fg", "gf", "eg", "gh"]:
        g.add_edge(u, v)
    return g


def main():
    print("small graph:", ["".join(c) for c in kosaraju(small())])
    print("roads, road 1 one-way:", [len(c) for c in kosaraju(roads())], "(sizes)")
    as_listed = Graph(directed=True)  # every road one-way, from from_place to to_place
    for r in rows("roads"):
        as_listed.add_edge(int(r["from_place"]), int(r["to_place"]))
    sizes = sorted((len(c) for c in kosaraju(as_listed)), reverse=True)
    print(f"every road one-way as listed: {len(sizes)} components, largest {sizes[0]}")

if __name__ == "__main__":
    main()
