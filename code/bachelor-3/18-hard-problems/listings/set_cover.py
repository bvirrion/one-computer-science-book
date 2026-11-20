"""set_cover.py -- greedy set cover: repeatedly take the set that covers most of what is
still uncovered. Within a factor H(n) of the minimum; here against the exact minimum."""
import itertools
import random


def greedy(universe, sets):
    uncovered, chosen = set(universe), []
    while uncovered:
        i = max(range(len(sets)), key=lambda i: len(sets[i] & uncovered))
        chosen.append(i)
        uncovered -= sets[i]
    return chosen


def exact(universe, sets):
    for k in range(1, len(sets) + 1):
        for c in itertools.combinations(range(len(sets)), k):
            if set().union(*(sets[i] for i in c)) >= set(universe):
                return list(c)


if __name__ == "__main__":
    # two halves of 1..14, against sets of sizes 8, 4, 2 that greedy prefers
    universe = range(1, 15)
    sets = [set(range(1, 8)), set(range(8, 15)),
            {1, 2, 3, 4, 8, 9, 10, 11}, {5, 6, 12, 13}, {7, 14}]
    print("greedy:", greedy(universe, sets), " exact:", exact(universe, sets))
    rng, ratios = random.Random(18), []
    for _ in range(200):
        n = 20
        sets = [set(rng.sample(range(n), rng.randrange(2, 8))) for _ in range(12)]
        if set().union(*sets) != set(range(n)):
            continue
        ratios.append(len(greedy(range(n), sets)) / len(exact(range(n), sets)))
    mean = sum(ratios) / len(ratios)
    print(f"{len(ratios)} random instances: mean ratio {mean:.3f}, "
          f"worst {max(ratios):.3f}")
