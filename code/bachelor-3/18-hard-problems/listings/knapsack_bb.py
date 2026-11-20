"""knapsack_bb.py -- 0-1 knapsack by branch and bound: take or leave each item, in order
of value per kilogram. With the fractional bound, a branch is cut when even filling the
rest of the bag with fractions of items could not beat the best bag found so far."""
import random


def fractional_bound(items, i, room, value):
    """The best value of the relaxed problem, where items may be cut."""
    for w, v in items[i:]:
        if w <= room:
            room, value = room - w, value + v
        else:
            return value + v * room / w
    return value


def branch_and_bound(items, capacity, use_bound):
    items = sorted(items, key=lambda it: it[1] / it[0], reverse=True)
    best, nodes = 0, 0

    def explore(i, room, value):
        nonlocal best, nodes
        nodes += 1
        best = max(best, value)
        if i == len(items):
            return
        if use_bound and fractional_bound(items, i, room, value) <= best:
            return  # prune: this branch cannot beat the best
        w, v = items[i]
        if w <= room:
            explore(i + 1, room - w, value + v)  # take item i
        explore(i + 1, room, value)  # leave it
    explore(0, capacity, 0)
    return best, nodes


if __name__ == "__main__":
    rng = random.Random(18)
    print(" n   best value   nodes, no bound   nodes, fractional bound")
    for n in (10, 14, 18, 22):
        items = [(rng.randrange(10, 60), rng.randrange(10, 60)) for _ in range(n)]
        capacity = sum(w for w, _ in items) // 2
        best, plain = branch_and_bound(items, capacity, False)
        same, bounded = branch_and_bound(items, capacity, True)
        assert best == same
        print(f"{n:>2}   {best:>10}   {plain:>15,}   {bounded:>23,}")
