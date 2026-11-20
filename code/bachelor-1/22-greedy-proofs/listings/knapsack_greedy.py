"""knapsack_greedy.py: the knapsack by value per unit of weight, against the optimum."""

import random


def greedy(items, capacity):
    """Take items by decreasing value/weight while they fit."""
    total = 0
    for w, v in sorted(items, key=lambda t: t[1] / t[0], reverse=True):
        if w <= capacity:
            capacity -= w
            total += v
    return total


def optimum(items, capacity):
    """The best value, by dynamic programming over the capacities (integer weights)."""
    best = [0] * (capacity + 1)  # best[c]: best value within capacity c, items so far
    for w, v in items:
        for c in range(capacity, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


def main():
    rng = random.Random(22)
    ratios = []
    for _ in range(1000):
        items = [(rng.randint(10, 60), rng.randint(10, 100)) for _ in range(12)]
        capacity = sum(w for w, _ in items) // 2
        ratios.append(greedy(items, capacity) / optimum(items, capacity))
    print(f"1000 random instances of 12 items: greedy optimal in "
          f"{sum(r == 1 for r in ratios)}, mean ratio {sum(ratios) / len(ratios):.4f},"
          f" worst {min(ratios):.3f}")
    items, capacity = [(1, 2), (100, 100)], 100
    print(f"items {items}, capacity {capacity}: greedy {greedy(items, capacity)},"
          f" optimum {optimum(items, capacity)}")


if __name__ == "__main__":
    main()
