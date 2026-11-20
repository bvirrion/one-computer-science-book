def has_cycle_undirected(g):
    """A cycle exists if the search meets a visited vertex other than its parent."""
    visited = set()
    for root in g:
        if root in visited:
            continue
        visited.add(root)
        stack = [(root, None)]
        while stack:
            v, parent = stack.pop()
            for w in g[v]:
                if w not in visited:
                    visited.add(w)
                    stack.append((w, v))
                elif w != parent:
                    return True
    return False


WHITE, GREY, BLACK = 0, 1, 2      # not seen, being explored, finished


def has_cycle_directed(g):
    colour = {v: WHITE for v in g}

    def explore(v):
        colour[v] = GREY
        for w in g[v]:
            if colour[w] == GREY:            # an edge back to a vertex in progress
                return True
            if colour[w] == WHITE and explore(w):
                return True
        colour[v] = BLACK
        return False

    return any(colour[v] == WHITE and explore(v) for v in g)


tree = {1: [2, 3], 2: [1, 4], 3: [1], 4: [2]}
square = {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [3, 1]}
print("tree:", has_cycle_undirected(tree), "| square:", has_cycle_undirected(square))
courses = {"maths": ["physics", "cs"], "physics": ["engineering"],
           "cs": ["engineering"], "engineering": []}
print("course prerequisites:", has_cycle_directed(courses))
courses["engineering"].append("maths")
print("with engineering -> maths:", has_cycle_directed(courses))
