"""quicksort.py: quicksort counting comparisons, with a fixed or a random pivot."""


def quicksort(a, pick, count):
    """Sort the list a of distinct keys; pick(a) chooses the pivot's index. Each element
    other than the pivot is compared with it once; count[0] adds them up."""
    if len(a) <= 1:
        return list(a)
    pivot = a[pick(a)]
    count[0] += len(a) - 1
    smaller = [x for x in a if x < pivot]
    larger = [x for x in a if x > pivot]
    return quicksort(smaller, pick, count) + [pivot] + quicksort(larger, pick, count)


def first(a):
    return 0


def random_pivot(rng):
    return lambda a: rng.randrange(len(a))


def shuffle(a, rng):
    """Fisher-Yates: position i receives a uniform choice among the positions >= i."""
    a = list(a)
    for i in range(len(a) - 1):
        j = rng.randrange(i, len(a))
        a[i], a[j] = a[j], a[i]
    return a
