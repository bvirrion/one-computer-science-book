"""Exercise 10: every subset of a small set, by a comprehension over bit patterns."""


def subsets(elements):
    """Return the list of all subsets of the list elements (no repeats), as sets."""
    n = len(elements)
    return [{elements[i] for i in range(n) if (k >> i) & 1} for k in range(2**n)]


if __name__ == "__main__":
    all_subsets = subsets(["a", "b", "c", "d"])
    print(len(all_subsets))
