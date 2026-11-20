"""find_cycle.py: a cycle of a directed graph, as a list of vertices, or None."""


def find_cycle(adj):
    state, parent = {}, {}  # state: 1 open, 2 finished

    def visit(u):
        state[u] = 1
        for v in adj[u]:
            if state.get(v) == 1:  # a back edge u -> v closes a cycle v ... u
                cycle = [u]
                while cycle[-1] != v:
                    cycle.append(parent[cycle[-1]])
                return cycle[::-1]
            if v not in state:
                parent[v] = u
                found = visit(v)
                if found:
                    return found
        state[u] = 2
        return None

    for s in adj:
        if s not in state:
            found = visit(s)
            if found:
                return found
    return None
