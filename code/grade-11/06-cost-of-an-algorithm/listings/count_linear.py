"""Linear search, counting its comparisons."""


def search(t, x):
    comparisons = 0
    for i in range(len(t)):
        comparisons += 1
        if t[i] == x:
            return i, comparisons
    return None, comparisons


if __name__ == "__main__":
    for n in [10, 100, 1000]:
        t = [f"name{k}" for k in range(n)]
        _, best = search(t, "name0")
        _, worst = search(t, "nobody")
        print(f"n = {n:4}: best case {best:4} comparison(s), worst case {worst:4}")
