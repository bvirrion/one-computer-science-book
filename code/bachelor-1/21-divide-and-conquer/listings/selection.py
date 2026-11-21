"""selection.py: the k-th smallest key, by quickselect and by the median of medians,
counting key comparisons."""

import random

comparisons = 0


def less(x, y):
    global comparisons
    comparisons += 1
    return x < y


def split(a, pivot):
    """The keys of a below, equal to and above pivot."""
    low, high = [x for x in a if less(x, pivot)], [x for x in a if less(pivot, x)]
    return low, len(a) - len(low) - len(high), high


def quickselect(a, k, rng=None):
    """The key of rank k (0 = smallest); pivot: the last key, or a random one."""
    while True:
        pivot = a[-1] if rng is None else rng.choice(a)
        low, equal, high = split(a, pivot)
        if k < len(low):
            a = low
        elif k < len(low) + equal:
            return pivot
        else:
            a, k = high, k - len(low) - equal


def sort5(g):
    """Insertion sort of a short list, counting comparisons."""
    g = list(g)
    for i in range(1, len(g)):
        j = i
        while j > 0 and less(g[j], g[j - 1]):
            g[j], g[j - 1] = g[j - 1], g[j]
            j -= 1
    return g


def mom_select(a, k):
    """The key of rank k, with the median of the medians of groups of five as pivot."""
    if len(a) <= 5:
        return sort5(a)[k]
    groups = [a[i:i + 5] for i in range(0, len(a), 5)]
    medians = [sort5(g)[(len(g) - 1) // 2] for g in groups]
    pivot = mom_select(medians, (len(medians) - 1) // 2)
    low, equal, high = split(a, pivot)
    if k < len(low):
        return mom_select(low, k)
    if k < len(low) + equal:
        return pivot
    return mom_select(high, k - len(low) - equal)


def count(f, *args):
    global comparisons
    comparisons = 0
    f(*args)
    return comparisons


def main():
    rng = random.Random(21)
    print(f"{'n':>6} {'quick, sorted':>13} {'quick, random':>13}"
          f" {'quick, rnd pivot':>16}"
          f" {'mom, sorted':>11} {'mom, random':>11}")
    for n in (1000, 2000, 4000, 8000):
        ordered = list(range(n))
        shuffled = rng.sample(range(n), n)
        k = n // 2  # the upper median: rank n/2
        row = [count(quickselect, ordered, k), count(quickselect, shuffled, k),
               count(quickselect, ordered, k, random.Random(n)),
               count(mom_select, ordered, k), count(mom_select, shuffled, k)]
        print(f"{n:6} {row[0]:13} {row[1]:13} {row[2]:16} {row[3]:11} {row[4]:11}")


if __name__ == "__main__":
    main()
