"""rag_cycle.py -- a resource-allocation graph, one instance of each resource: an edge
P -> R is a request, R -> P a holding. A cycle means deadlock; a depth-first search
finds one."""


def find_cycle(graph):
    colour = {v: "white" for v in graph}  # unseen, on the path, or done
    path = []

    def visit(v):
        colour[v] = "grey"
        path.append(v)
        for w in graph[v]:
            if colour[w] == "grey":  # back to the path: a cycle
                return path[path.index(w):] + [w]
            if colour[w] == "white" and (found := visit(w)):
                return found
        colour[v] = "black"
        path.pop()
        return None

    for v in graph:
        if colour[v] == "white" and (found := visit(v)):
            return found
    return None


if __name__ == "__main__":
    GRAPH = {"P1": ["R2"], "P2": ["R3"], "P3": ["R1"], "P4": ["R2"],
             "R1": ["P1"], "R2": ["P2"], "R3": ["P3"]}
    print("cycle:", " -> ".join(find_cycle(GRAPH)))
    GRAPH["P3"] = []  # P3 no longer waits for R1
    print("after P3's request is withdrawn:", find_cycle(GRAPH))
