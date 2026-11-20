"""enumerate.py: all subsets, permutations and combinations of a small collection."""


def subsets_binary(items):
    """Subset number x holds items[i] exactly when bit i of x is 1."""
    n = len(items)
    for x in range(2**n):
        yield [items[i] for i in range(n) if x >> i & 1]


def subsets(items, chosen=()):
    """The include/exclude tree: decide items[0], then the rest."""
    if not items:
        yield list(chosen)
        return
    yield from subsets(items[1:], chosen + (items[0],))  # with items[0]
    yield from subsets(items[1:], chosen)  # without it


def permutations(a, k=0):
    """All orders of a[k:], by swapping each candidate into position k in turn."""
    if k == len(a):
        yield list(a)
        return
    for i in range(k, len(a)):
        a[k], a[i] = a[i], a[k]
        yield from permutations(a, k + 1)
        a[k], a[i] = a[i], a[k]  # undo, so that a[k:] is as before


def next_permutation(a):
    """The next order of a in lexicographic order, in place; False after the last."""
    i = len(a) - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1  # a[i+1:] is decreasing: the last order of its elements
    if i < 0:
        return False
    j = len(a) - 1
    while a[j] <= a[i]:
        j -= 1  # the smallest element of a[i+1:] larger than a[i]
    a[i], a[j] = a[j], a[i]
    a[i + 1:] = reversed(a[i + 1:])  # the first order of the suffix
    return True


def combinations(items, k, start=0, chosen=()):
    """The k-element subsets of items[start:], in increasing order of positions."""
    if len(chosen) == k:
        yield list(chosen)
        return
    for i in range(start, len(items) - (k - len(chosen)) + 1):  # room for the rest
        yield from combinations(items, k, i + 1, chosen + (items[i],))


def main():
    print("subsets by bits:", [''.join(s) for s in subsets_binary("abc")])
    print("subsets by tree:", [''.join(s) for s in subsets("abc")])
    print("permutations   :", [''.join(p) for p in permutations(list("abc"))])
    a, order = list("abcd"), []
    while True:
        order.append(''.join(a))
        if not next_permutation(a):
            break
    print("lexicographic  :", len(order), "orders,", order[:4], "...", order[-1])
    print("2 of abcd      :", [''.join(c) for c in combinations("abcd", 2)])
    print("counts         : subsets of 10:", sum(1 for _ in subsets(range(10))),
          "orders of 8:", sum(1 for _ in permutations(list(range(8)))),
          "4 of 10:", sum(1 for _ in combinations(range(10), 4)))


if __name__ == "__main__":
    main()
