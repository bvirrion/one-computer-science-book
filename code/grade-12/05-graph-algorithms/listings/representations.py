"""One graph, two representations: adjacency lists and adjacency matrix."""
G = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D", "E"],
     "D": ["B", "C", "F"], "E": ["C", "F"], "F": ["D", "E"]}


def to_matrix(adj):
    names = sorted(adj)
    index = {v: i for i, v in enumerate(names)}
    m = [[0] * len(names) for _ in names]
    for v in adj:
        for w in adj[v]:
            m[index[v]][index[w]] = 1
    return names, m


def to_lists(names, m):
    return {v: [names[j] for j, x in enumerate(row) if x] for v, row in zip(names, m)}


if __name__ == "__main__":
    names, m = to_matrix(G)
    for v, row in zip(names, m):
        print(v, row, "| neighbours:", G[v])
    print("back to lists, same graph:", to_lists(names, m) == G)

    # a directed graph: successors are given, predecessors are computed
    succ = {"wake": ["dress", "eat"], "dress": ["leave"], "eat": ["leave"], "leave": []}
    pred = {v: [u for u in succ if v in succ[u]] for v in succ}
    print("predecessors:", pred)
