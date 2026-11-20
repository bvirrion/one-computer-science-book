"""min_swaps.py: the fewest swaps that sort a list of 0, 1 and 2."""


def min_swaps(a):
    """c[i][j]: elements of value i lying in the region where value j belongs.
    A pair i <-> j of misplaced elements is fixed by one swap; what remains
    forms cycles of three elements, each fixed by two swaps."""
    bounds = [0, a.count(0), a.count(0) + a.count(1), len(a)]
    c = [[0] * 3 for _ in range(3)]
    for j in range(3):
        for x in a[bounds[j]:bounds[j + 1]]:
            c[x][j] += 1
    pairs = sum(min(c[i][j], c[j][i]) for i in range(3) for j in range(i + 1, 3))
    left = sum(c[i][j] for i in range(3) for j in range(3) if i != j) - 2 * pairs
    return pairs + 2 * (left // 3)
