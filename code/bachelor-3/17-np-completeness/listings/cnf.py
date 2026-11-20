"""cnf.py -- formulas in conjunctive normal form, as lists of clauses; a clause is a
list of literals, +i for x_i and -i for not x_i, variables numbered from 1. Brute-force
helpers used to check every reduction of the chapter on small instances."""
import itertools
import random


def satisfies(clauses, assignment):
    """assignment maps a variable to True or False."""
    return all(any(assignment[abs(x)] == (x > 0) for x in c) for c in clauses)


def variables(clauses):
    return sorted({abs(x) for c in clauses for x in c})


def brute_force(clauses):
    """A satisfying assignment, or None, by trying all of them."""
    vs = variables(clauses)
    for bits in itertools.product((False, True), repeat=len(vs)):
        a = dict(zip(vs, bits))
        if satisfies(clauses, a):
            return a
    return None


def random_3cnf(n, m, rng):
    """m clauses of three literals on three different variables among x_1..x_n."""
    return [[rng.choice((1, -1)) * v for v in rng.sample(range(1, n + 1), 3)]
            for _ in range(m)]


def has_independent_set(n, edges, k):
    adjacent = set(edges) | {(v, u) for u, v in edges}
    return any(all((a, b) not in adjacent for a, b in itertools.combinations(s, 2))
               for s in itertools.combinations(range(n), k))


def is_colourable(n, edges, colours):
    """Backtracking: colour vertices 0, 1, ... in order, never clashing with a
    neighbour already coloured. Exponential in the worst case, fast on small graphs."""
    before = {v: [] for v in range(n)}
    for u, v in edges:
        before[max(u, v)].append(min(u, v))
    colour = []

    def extend(v):
        if v == n:
            return True
        for c in range(colours):
            if all(colour[u] != c for u in before[v]):
                colour.append(c)
                if extend(v + 1):
                    return True
                colour.pop()
        return False
    return extend(0)


def subset_sums_to(numbers, target):
    reachable = {0}
    for x in numbers:
        reachable |= {s + x for s in reachable if s + x <= target}
    return target in reachable


if __name__ == "__main__":
    print(brute_force(random_3cnf(4, 6, random.Random(1))))
