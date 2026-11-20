"""ex5_hampath.py -- exercise 5: a Hamiltonian-path verifier that accepts a walk which
repeats a vertex, and its fix."""


def buggy(n, edges, order):
    adjacent = set(edges) | {(v, u) for u, v in edges}
    return len(order) == n and all((u, v) in adjacent for u, v in zip(order, order[1:]))


def fixed(n, edges, order):
    # the fix: every vertex exactly once, i.e. order is a permutation of 0..n-1
    return sorted(order) == list(range(n)) and buggy(n, edges, order)
