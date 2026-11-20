"""Two processes each add 1 to a shared counter, in three steps: every interleaving."""
from itertools import combinations


def steps(name):
    """counter += 1, as the processor does it: load, add, store."""
    return [(name, "load"), (name, "add"), (name, "store")]


def run(schedule):
    counter, register = 0, {}
    for name, action in schedule:
        if action == "load":
            register[name] = counter             # copy the shared value
        elif action == "add":
            register[name] += 1                  # change the private copy
        else:
            counter = register[name]             # write the copy back
    return counter


def interleavings(p, q):
    """Every order of the steps of p and q that keeps each one's own order."""
    n = len(p) + len(q)
    for places in combinations(range(n), len(p)):   # where p's steps go
        it_p, it_q = iter(p), iter(q)
        yield [next(it_p) if k in places else next(it_q) for k in range(n)]


if __name__ == "__main__":
    results = [run(s) for s in interleavings(steps("P"), steps("Q"))]
    print(len(results), "interleavings:", results.count(2), "give 2,",
          results.count(1), "give 1 (an update lost)")
    bad = next(s for s in interleavings(steps("P"), steps("Q")) if run(s) == 1)
    print("for instance:", ", ".join(f"{n} {a}" for n, a in bad))
