"""exo_knapsack_up.py: exercise 5, the knapsack on one row, capacities taken upwards."""


def one_row(items, capacity, downwards):
    best = [0] * (capacity + 1)
    for w, v in items:
        order = range(capacity, w - 1, -1) if downwards else range(w, capacity + 1)
        for c in order:
            best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


if __name__ == "__main__":
    items = [(3, 25), (4, 40), (2, 15)]
    print("downwards:", one_row(items, 8, True), " upwards:", one_row(items, 8, False))
