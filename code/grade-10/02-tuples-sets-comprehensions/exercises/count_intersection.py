"""Exercise 12: comparisons made by a list-based intersection."""


def list_intersection(a, b):
    """Return the elements of a that are in b, and the number of == comparisons made."""
    comparisons = 0
    result = []
    for x in a:
        for y in b:
            comparisons += 1
            if x == y:
                result.append(x)
                break
    return result, comparisons
