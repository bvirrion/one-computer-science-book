"""two_sat.py -- 2-SAT in linear time. Each clause (a or b) gives two implications,
not a -> b and not b -> a. The formula is unsatisfiable exactly when some x and not x
lie in the same strongly connected component of this implication graph."""


def implication_graph(clauses, n):
    graph = {lit: [] for v in range(1, n + 1) for lit in (v, -v)}
    for a, b in clauses:
        graph[-a].append(b)
        graph[-b].append(a)
    return graph


def components(graph):
    """Kosaraju: order by finishing time, then search the reversed graph."""
    order, seen = [], set()
    for start in graph:
        if start in seen:
            continue
        seen.add(start)
        stack = [(start, iter(graph[start]))]
        while stack:  # depth-first search without recursion
            v, it = stack[-1]
            w = next((w for w in it if w not in seen), None)
            if w is None:
                order.append(v)
                stack.pop()
            else:
                seen.add(w)
                stack.append((w, iter(graph[w])))
    reverse = {v: [] for v in graph}
    for v in graph:
        for w in graph[v]:
            reverse[w].append(v)
    comp, count = {}, 0
    for root in reversed(order):  # components come out in topological order
        if root in comp:
            continue
        comp[root], stack = count, [root]
        while stack:
            for w in reverse[stack.pop()]:
                if w not in comp:
                    comp[w] = count
                    stack.append(w)
        count += 1
    return comp


def solve(clauses, n):
    comp = components(implication_graph(clauses, n))
    if any(comp[v] == comp[-v] for v in range(1, n + 1)):
        return None
    # x is true when its component comes later in topological order than not x's
    return {v: comp[v] > comp[-v] for v in range(1, n + 1)}


if __name__ == "__main__":
    f = [(1, 2), (-1, 3), (-2, -3), (2, 4), (-4, -1)]
    print("formula:", f)
    comp = components(implication_graph(f, 4))
    print("components:", {c: sorted((v for v in comp if comp[v] == c), key=abs)
                          for c in sorted(set(comp.values()))})
    print("assignment:", solve(f, 4))
    g = f + [(1, -2), (-1, -2)]
    print("with (x1 or not x2) and (not x1 or not x2):", solve(g, 4))
