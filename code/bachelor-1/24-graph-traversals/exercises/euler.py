"""euler.py: an Euler circuit (every edge once) of a connected graph whose
degrees are all even, by Hierholzer's method: follow edges until stuck, splice in
the detours."""


def euler_circuit(edges, start):
    """edges: list of (u, v), undirected. Returns the circuit as a list of vertices."""
    adj = {}
    for i, (u, v) in enumerate(edges):
        adj.setdefault(u, []).append((v, i))
        adj.setdefault(v, []).append((u, i))
    used, stack, circuit = set(), [start], []
    while stack:
        u = stack[-1]
        while adj[u] and adj[u][-1][1] in used:
            adj[u].pop()  # drop edges already walked
        if adj[u]:
            v, i = adj[u].pop()
            used.add(i)
            stack.append(v)  # walk on
        else:
            circuit.append(stack.pop())  # stuck: u is final, back up
    return circuit[::-1]
