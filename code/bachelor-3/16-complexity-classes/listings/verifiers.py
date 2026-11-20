"""verifiers.py -- certificate checkers for three problems in NP. Each counts its basic
steps (one per element or edge looked at), to show that checking is fast."""
import random


def subset_sum(numbers, target, chosen):
    """Certificate: a list of distinct indices whose numbers add up to target."""
    steps, total, seen = 0, 0, set()
    for i in chosen:
        steps += 1
        if i in seen or not 0 <= i < len(numbers):
            return False, steps
        seen.add(i)
        total += numbers[i]
    return total == target, steps


def hamiltonian_path(n, edges, order):
    """Certificate: the vertices 0..n-1, each once, consecutive ones adjacent."""
    steps, adjacent = len(edges), set(edges) | {(v, u) for u, v in edges}
    if sorted(order) != list(range(n)):
        return False, steps + n
    for u, v in zip(order, order[1:]):
        steps += 1
        if (u, v) not in adjacent:
            return False, steps
    return True, steps


def three_colouring(n, edges, colour):
    """Certificate: a colour 0, 1 or 2 per vertex, the ends of each edge different."""
    steps = n
    if len(colour) != n or any(c not in (0, 1, 2) for c in colour):
        return False, steps
    for u, v in edges:
        steps += 1
        if colour[u] == colour[v]:
            return False, steps
    return True, steps


def instance(n, rng):
    """A graph with 2n edges, a Hamiltonian path hidden in it, and a 3-colouring."""
    order = rng.sample(range(n), n)
    colour = [0] * n
    for i, v in enumerate(order):
        colour[v] = i % 3  # consecutive vertices of the path get different colours
    edges = list(zip(order, order[1:]))
    while len(edges) < 2 * n:
        u, v = rng.sample(range(n), 2)
        if colour[u] != colour[v]:
            edges.append((u, v))
    return order, edges, colour


if __name__ == "__main__":
    rng = random.Random(16)
    print("    n   subset sum   Hamiltonian path   3-colouring   (steps, all accepted)")
    for n in (10, 100, 1000, 10000):
        numbers = [rng.randrange(1, 1000) for _ in range(n)]
        chosen = rng.sample(range(n), n // 2)
        target = sum(numbers[i] for i in chosen)
        order, edges, colour = instance(n, rng)
        checks = [subset_sum(numbers, target, chosen),
                  hamiltonian_path(n, edges, order), three_colouring(n, edges, colour)]
        assert all(ok for ok, _ in checks)
        print(f"{n:>5}   {checks[0][1]:>10}   {checks[1][1]:>16}   {checks[2][1]:>11}")
