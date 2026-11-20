"""reduce_is.py -- 3-SAT to independent set: one vertex per literal of each clause, a
triangle per clause, an edge between complementary literals; k = number of clauses.
Then independent set to clique (complement graph) and to vertex cover (n - k)."""
import itertools
import random

from cnf import brute_force, has_independent_set, random_3cnf


def to_independent_set(clauses):
    vertices = [(j, lit) for j, c in enumerate(clauses) for lit in c]
    edges = []
    for a, b in itertools.combinations(range(len(vertices)), 2):
        (ja, la), (jb, lb) = vertices[a], vertices[b]
        if ja == jb or la == -lb:  # same clause, or contradictory literals
            edges.append((a, b))
    return vertices, edges, len(clauses)


def to_clique(n, edges, k):
    """An independent set of G is a clique of the complement of G."""
    present = set(edges)
    return n, [e for e in itertools.combinations(range(n), 2) if e not in present], k


def to_vertex_cover(n, edges, k):
    """S is independent if and only if the other n - |S| vertices cover every edge."""
    return n, edges, n - k


if __name__ == "__main__":
    formula = [[1, -2, 3], [-1, 2, 3], [-1, -2, -3]]
    vertices, edges, k = to_independent_set(formula)
    print(f"{len(vertices)} vertices, {len(edges)} edges, k = {k}")
    print("vertices:", vertices)
    n = len(vertices)
    print("clique instance: k =", to_clique(n, edges, k)[2],
          "edges", len(to_clique(n, edges, k)[1]),
          "; vertex cover instance: k =", to_vertex_cover(n, edges, k)[2])
    rng, agree = random.Random(17), 0
    for _ in range(200):
        f = random_3cnf(4, rng.randrange(1, 7), rng)
        _, e, kk = to_independent_set(f)
        agree += (brute_force(f) is not None) == has_independent_set(3 * len(f), e, kk)
    print(f"satisfiable = has an independent set of size k: {agree} of 200 "
          f"random formulas")
