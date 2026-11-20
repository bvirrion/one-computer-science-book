def remove_negatives_buggy(t):
    for x in t:
        if x < 0:
            t.remove(x)
    return t


def remove_negatives(t):
    """Return a new list holding the elements of t that are not negative."""
    result = []
    for x in t:
        if x >= 0:
            result.append(x)
    return result
