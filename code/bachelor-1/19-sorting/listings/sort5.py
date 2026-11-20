"""sort5.py: five keys in seven comparisons by merge insertion, checked on all 120
orders, against insertion sort and merge sort."""

from collections import Counter
from itertools import permutations


class Counted:
    """A key that counts the comparisons made with it."""

    calls = 0

    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        Counted.calls += 1
        return self.v < other.v


def insert(chain, x, hi):
    """Insert x into the sorted chain[0:hi] by binary search."""
    lo = 0
    while lo < hi:
        mid = (lo + hi) // 2
        if x < chain[mid]:
            hi = mid
        else:
            lo = mid + 1
    chain.insert(lo, x)


def merge_insertion5(a, b, c, d, e):
    if b < a:  # 1: order the pair (a, b)
        a, b = b, a
    if d < c:  # 2: order the pair (c, d)
        c, d = d, c
    if d < b:  # 3: order the pairs by their larger keys: a < b < d and c < d
        a, b, c, d = c, d, a, b
    chain = [a, b, d]
    insert(chain, e, 3)  # 4, 5: e into a chain of three
    insert(chain, c, chain.index(d))  # 6, 7: c among the keys below d, at most three
    return chain


def insertion_sort(xs):
    xs = list(xs)
    for i in range(1, len(xs)):
        j = i
        while j > 0 and xs[j] < xs[j - 1]:
            xs[j], xs[j - 1] = xs[j - 1], xs[j]
            j -= 1
    return xs


def merge_sort(xs):
    if len(xs) < 2:
        return list(xs)
    left, right = merge_sort(xs[: len(xs) // 2]), merge_sort(xs[len(xs) // 2:])
    out = []
    while left and right:
        out.append(right.pop(0) if right[0] < left[0] else left.pop(0))
    return out + left + right


def survey(method):
    """The counts of comparisons over the 120 orders, after checking every result."""
    counts = Counter()
    for order in permutations(range(5)):
        Counted.calls = 0
        result = method([Counted(v) for v in order])
        assert [k.v for k in result] == [0, 1, 2, 3, 4]
        counts[Counted.calls] += 1
    return counts


def main():
    methods = [("insertion sort", insertion_sort), ("merge sort", merge_sort),
               ("merge insertion", lambda ks: merge_insertion5(*ks))]
    for name, method in methods:
        counts = survey(method)
        mean = sum(c * k for c, k in counts.items()) / 120
        spread = dict(sorted(counts.items()))
        print(f"{name:15} worst {max(counts)}, mean {mean:.2f}, counts {spread}")


if __name__ == "__main__":
    main()
