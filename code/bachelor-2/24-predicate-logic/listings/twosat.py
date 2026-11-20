"""twosat.py: 2-CNF satisfiability through the implication graph and its strongly
connected components (Kosaraju's two searches)."""


def solve(n, clauses):
    """Variables 1..n; a literal is k or -k; a clause (a, b) means a | b.
    Returns a satisfying assignment {k: bool}, or the variable and its component."""
    def node(lit):  # the vertex of x_k is 2k - 2, that of ~x_k is 2k - 1
        return 2 * (abs(lit) - 1) + (lit < 0)

    succ = [[] for _ in range(2 * n)]
    pred = [[] for _ in range(2 * n)]
    for a, b in clauses:  # a | b gives ~a -> b and ~b -> a
        for u, v in [(node(-a), node(b)), (node(-b), node(a))]:
            succ[u].append(v)
            pred[v].append(u)
    order, seen = [], [False] * (2 * n)
    for start in range(2 * n):  # first search: the vertices by finishing time
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, iter(succ[start]))]
        while stack:
            u, it = stack[-1]
            v = next((v for v in it if not seen[v]), None)
            if v is None:
                order.append(u)
                stack.pop()
            else:
                seen[v] = True
                stack.append((v, iter(succ[v])))
    comp = [-1] * (2 * n)
    count = 0
    for start in reversed(order):  # second search, on the reversed graph
        if comp[start] >= 0:
            continue
        comp[start], todo = count, [start]
        while todo:
            u = todo.pop()
            for v in pred[u]:
                if comp[v] < 0:
                    comp[v] = count
                    todo.append(v)
        count += 1  # components numbered in a topological order of the graph
    for k in range(1, n + 1):
        if comp[node(k)] == comp[node(-k)]:
            return None, k
    # x_k is true when its component comes after that of ~x_k in topological order
    return {k: comp[node(k)] > comp[node(-k)] for k in range(1, n + 1)}, None
