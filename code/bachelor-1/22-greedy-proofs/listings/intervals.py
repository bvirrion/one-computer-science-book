"""intervals.py: one room, many talks: four greedy rules against the true optimum."""

import random
from itertools import combinations

RULES = {
    "earliest finish": lambda t, talks: t[1],
    "earliest start": lambda t, talks: t[0],
    "shortest": lambda t, talks: t[1] - t[0],
    "fewest conflicts": lambda t, talks: sum(overlap(t, u) for u in talks),
}


def overlap(t, u):
    """Do the talks [start, end) t and u overlap?"""
    return t[0] < u[1] and u[0] < t[1]


def greedy(talks, rule):
    """Take the talks in the rule's order, keeping each one compatible with the kept."""
    kept = []
    for t in sorted(talks, key=lambda t: RULES[rule](t, talks)):
        if all(not overlap(t, u) for u in kept):
            kept.append(t)
    return sorted(kept)


def optimum(talks):
    """The largest number of pairwise compatible talks, by trying all subsets."""
    for k in range(len(talks), 0, -1):
        for chosen in combinations(talks, k):
            if all(not overlap(a, b) for a, b in combinations(chosen, 2)):
                return k
    return 0


def random_talks(rng, n, day=600):
    """n talks of 20 to 120 minutes in a day of `day` minutes."""
    talks = []
    for _ in range(n):
        length = rng.randint(20, 120)
        start = rng.randint(0, day - length)
        talks.append((start, start + length))
    return talks


def main():
    rng = random.Random(22)
    conference = random_talks(rng, 40)
    best = greedy(conference, "earliest finish")
    print(f"40 talks, one room: {len(best)} fit, ending at", [t[1] for t in best])
    wins = {rule: 0 for rule in RULES}
    for _ in range(500):
        talks = random_talks(rng, 10)
        opt = optimum(talks)
        for rule in RULES:
            wins[rule] += len(greedy(talks, rule)) == opt
    print("optimal on 500 random sets of 10 talks:")
    for rule, w in wins.items():
        print(f"  {rule:16} {w:3}")


if __name__ == "__main__":
    main()
