"""heights_sum.py: the heights of the nodes of a heap of n nodes add up to n - v(n),
where v(n) is the number of ones in the binary writing of n; checked for n <= 10^4."""


def heights(n):
    """h[i] = the height of node i in a complete tree of n nodes stored as a heap."""
    h = [0] * n
    for i in range(n - 1, -1, -1):
        children = [h[c] for c in (2 * i + 1, 2 * i + 2) if c < n]
        h[i] = 1 + max(children) if children else 0
    return h


def sums_of_heights(limit):
    """[S(0), ..., S(limit)]: the tree grows one leaf at a time, raising ancestors."""
    h, total, sums = [], 0, [0]
    for i in range(limit):
        h.append(0)  # the new leaf, index i
        node, d = i, 0
        while node > 0:
            node, d = (node - 1) // 2, d + 1
            if h[node] >= d:
                break  # this ancestor, and so the ones above, are high enough
            total += d - h[node]
            h[node] = d
        sums.append(total)
    return sums


def nu(n):
    return bin(n).count("1")


def main():
    sums = sums_of_heights(10000)
    print(f"{'n':>6} {'sum of heights':>15} {'n - v(n)':>9}")
    for n in [1, 2, 3, 7, 10, 100, 1000, 1023, 1024, 10000]:
        assert sums[n] == sum(heights(n))
        print(f"{n:6} {sums[n]:15} {n - nu(n):9}")
    bad = [n for n in range(1, 10001) if sums[n] != n - nu(n)]
    print("n <= 10000 where they differ:", bad if bad else "none")


if __name__ == "__main__":
    main()
