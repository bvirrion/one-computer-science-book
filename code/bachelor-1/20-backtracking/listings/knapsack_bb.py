"""knapsack_bb.py: the 0/1 knapsack by plain backtracking and by branch and bound,
with the continuous relaxation (fractions of items allowed) as the bound."""

import random


def items(n, seed=20):
    rng = random.Random(seed)
    return [(rng.randint(10, 60), rng.randint(10, 100)) for _ in range(n)]  # (w, v)


def relaxation(things, i, room):
    """The best value of things[i:] in `room` if fractions of items were allowed:
    greedy by value per unit of weight (things are sorted that way)."""
    total = 0.0
    for w, v in things[i:]:
        if w <= room:
            room, total = room - w, total + v
        else:
            return total + v * room / w  # a fraction of the first item too big
    return total


def best(things, capacity, bound):
    things = sorted(things, key=lambda t: t[1] / t[0], reverse=True)
    stats = {"best": 0, "nodes": 0}

    def visit(i, room, value):
        stats["nodes"] += 1
        stats["best"] = max(stats["best"], value)
        if i == len(things):
            return
        if bound and value + relaxation(things, i, room) <= stats["best"]:
            return  # no completion can beat the best solution found so far
        w, v = things[i]
        if w <= room:
            visit(i + 1, room - w, value + v)  # take item i
        visit(i + 1, room, value)  # leave it

    visit(0, capacity, 0)
    return stats["best"], stats["nodes"]


def main():
    print(f"{'n':>2} {'best':>5} {'nodes, backtracking':>19} "
          f"{'nodes, branch and bound':>23}")
    for n in (8, 12, 16, 20):
        things = items(n)
        capacity = sum(w for w, _ in things) // 2
        b1, plain = best(things, capacity, bound=False)
        b2, bb = best(things, capacity, bound=True)
        assert b1 == b2
        print(f"{n:2} {b1:5} {plain:19} {bb:23}")


if __name__ == "__main__":
    main()
