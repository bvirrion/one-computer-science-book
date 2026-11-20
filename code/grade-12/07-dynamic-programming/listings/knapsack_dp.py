"""The 0/1 knapsack: best value with whole objects, by a table."""
from itertools import combinations


def knapsack(objects, capacity):
    """k[i][w]: best value with the first i objects and at most w kilograms."""
    n = len(objects)
    k = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, kg, value = objects[i - 1]
        for w in range(capacity + 1):
            k[i][w] = k[i - 1][w]                     # without object i
            if kg <= w and k[i - 1][w - kg] + value > k[i][w]:
                k[i][w] = k[i - 1][w - kg] + value    # with object i
    return k


def chosen(objects, k, capacity):
    names, w = [], capacity
    for i in range(len(objects), 0, -1):              # from the last object back
        if k[i][w] != k[i - 1][w]:                    # object i was taken
            names.append(objects[i - 1][0])
            w -= objects[i - 1][1]
    return names[::-1]


def every_subset(objects, capacity):
    return max(sum(o[2] for o in s) for r in range(len(objects) + 1)
               for s in combinations(objects, r) if sum(o[1] for o in s) <= capacity)


if __name__ == "__main__":
    small = [("A", 6, 30), ("B", 5, 20), ("C", 5, 20)]
    k = knapsack(small, 10)
    for i, row in enumerate(k):
        print(i, " ".join(f"{x:2}" for x in row))
    print("best", k[3][10], chosen(small, k, 10))
    pack = [("tent", 5, 60), ("stove", 3, 50), ("rope", 4, 40), ("camera", 2, 45),
            ("books", 6, 30), ("food", 4, 70), ("lamp", 1, 15), ("chair", 5, 35)]
    k = knapsack(pack, 15)
    print("best", k[len(pack)][15], chosen(pack, k, 15), "| every subset:",
          every_subset(pack, 15))
