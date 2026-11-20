"""Edit distance between two sequences, and the alignment that achieves it."""


def distance_table(a, b):
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]   # d[i][j]: from a[:i] to b[:j]
    for i in range(n + 1):
        d[i][0] = i                             # delete all i items
    for j in range(m + 1):
        d[0][j] = j                             # insert all j items
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            change = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j - 1] + change,   # keep or replace
                          d[i - 1][j] + 1,            # delete a[i - 1]
                          d[i][j - 1] + 1)            # insert b[j - 1]
    return d


def alignment(a, b, d):
    """Pairs (x, y) from the end back; None marks a gap."""
    i, j, pairs = len(a), len(b), []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1] and d[i][j] == d[i - 1][j - 1]:
            pairs.append((a[i - 1], b[j - 1]))        # kept
            i, j = i - 1, j - 1
        elif i > 0 and d[i][j] == d[i - 1][j] + 1:
            pairs.append((a[i - 1], None))            # deleted
            i -= 1
        elif j > 0 and d[i][j] == d[i][j - 1] + 1:
            pairs.append((None, b[j - 1]))            # inserted
            j -= 1
        else:
            pairs.append((a[i - 1], b[j - 1]))        # replaced
            i, j = i - 1, j - 1
    return pairs[::-1]


def show(pairs):
    """Three lines: the first version, the marks, the second version."""
    top, mid, bottom = [], [], []
    for x, y in pairs:
        width = max(len(x or "-"), len(y or "-"))
        top.append((x or "-" * width).ljust(width))
        mid.append(("|" if x == y else " " if x is None or y is None else "*") * width)
        bottom.append((y or "-" * width).ljust(width))
    return top, mid, bottom


if __name__ == "__main__":
    a = "the market opens at seven on sundays".split()
    b = "the new market opens at eight on sunday".split()
    d = distance_table(a, b)
    print("distance in words:", d[len(a)][len(b)])
    for line in show(alignment(a, b, d)):
        print(" ".join(line).rstrip())
