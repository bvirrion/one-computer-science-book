"""ex6_clique.py -- exercise 6: verify a certificate for "the graph has a clique of k
vertices" in O(m + k^2) steps: the edges go into a set once, then each pair is
looked up."""


def verify_clique(n, edges, k, chosen):
    if len(chosen) != k or len(set(chosen)) != k or not all(0 <= v < n for v in chosen):
        return False
    adjacent = set(edges) | {(v, u) for u, v in edges}
    return all((chosen[i], chosen[j]) in adjacent
               for i in range(k) for j in range(i + 1, k))
