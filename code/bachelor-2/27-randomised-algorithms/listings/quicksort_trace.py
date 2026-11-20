"""quicksort_trace.py: the pivots of one run of randomised quicksort on ten first
names, as a tree: each pivot's left subtree sorts the smaller names."""
import random

from town import people

rng = random.Random(21)


def tree(a, depth=0):
    if not a:
        return 0
    pivot = a[rng.randrange(len(a))]
    print("    " * depth + pivot + (f" ({len(a) - 1} compared)" if len(a) > 1 else ""))
    return (len(a) - 1 + tree([x for x in a if x < pivot], depth + 1)
            + tree([x for x in a if x > pivot], depth + 1))


names = sorted({p[1] for p in people()})[:10]
print("sorted input:", " ".join(names))
print("total", tree(names), "comparisons")
