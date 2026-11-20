"""knapsack.py: the 0/1 knapsack by a table over items and capacities, with the choice
of items rebuilt from the table."""

import random


def knapsack(items, capacity):
    """best[i][c]: the best value of the first i items within capacity c."""
    best = [[0] * (capacity + 1) for _ in range(len(items) + 1)]
    for i, (w, v) in enumerate(items, start=1):
        for c in range(capacity + 1):
            best[i][c] = best[i - 1][c]  # without item i
            if w <= c:
                best[i][c] = max(best[i][c], best[i - 1][c - w] + v)  # with it
    return best


def chosen(items, best, capacity):
    """Walk back: item i was taken where the value changed from row i - 1."""
    take, c = [], capacity
    for i in range(len(items), 0, -1):
        if best[i][c] != best[i - 1][c]:
            take.append(i - 1)
            c -= items[i - 1][0]
    return sorted(take)


def main():
    items = [(3, 25), (4, 40), (2, 15), (5, 50), (1, 8)]  # (weight, value)
    best = knapsack(items, 8)
    print("capacity: " + " ".join(f"{c:3}" for c in range(9)))
    for i, row in enumerate(best):
        label = "none" if i == 0 else f"+{items[i - 1]}"
        print(f"{label:>9} " + " ".join(f"{x:3}" for x in row))
    take = chosen(items, best, 8)
    print("take items", take, "value", best[-1][8])
    rng = random.Random(23)
    things = [(rng.randint(10, 60), rng.randint(10, 100)) for _ in range(40)]
    cap = sum(w for w, _ in things) // 2
    print(f"40 random items, capacity {cap}: best {knapsack(things, cap)[-1][cap]},"
          f" {41 * (cap + 1)} cells")


if __name__ == "__main__":
    main()
