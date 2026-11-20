"""exo_cover.py: a minimum vertex cover from a maximum matching (Konig)."""
import itertools

from matching import max_matching


def vertex_cover(adj, match):
    """Z: what alternating paths reach from the free left vertices; the cover is the
    left vertices outside Z and the right vertices inside Z."""
    partner = {u: v for v, u in match.items()}
    z_left = [u for u in adj if u not in partner]
    z_right, todo = set(), list(z_left)
    z_left = set(z_left)
    while todo:
        u = todo.pop()
        for v in adj[u]:  # a non-matching edge to the right
            if v not in z_right:
                z_right.add(v)
                w = match.get(v)  # then the matching edge back to the left
                if w is not None and w not in z_left:
                    z_left.add(w)
                    todo.append(w)
    return [u for u in adj if u not in z_left] + sorted(z_right)


ADJ = {"Ada": ["Mon", "Tue"], "Ben": ["Mon"], "Cy": ["Tue", "Wed", "Thu"],
       "Dee": ["Wed", "Fri"], "Eve": ["Mon", "Wed"], "Fay": ["Mon", "Tue"]}
match = max_matching(ADJ)
cover = vertex_cover(ADJ, match)
assert all(u in cover or v in cover for u in ADJ for v in ADJ[u])
print(f"matching of size {len(match)}; cover of size {len(cover)}: {cover}")
vertices = list(ADJ) + sorted({v for vs in ADJ.values() for v in vs})
smallest = next(k for k in range(len(vertices) + 1)
                for c in itertools.combinations(vertices, k)
                if all(u in c or v in c for u in ADJ for v in ADJ[u]))
print("smallest cover by trying all subsets:", smallest)
