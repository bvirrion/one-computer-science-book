"""distinct_parts.py: all ways to write n as a sum of distinct positive parts."""


def distinct_parts(n, largest=None):
    """The partitions of n into distinct parts <= largest, each list decreasing."""
    if largest is None:
        largest = n
    if n == 0:
        yield []
        return
    for part in range(min(n, largest), 0, -1):
        if part * (part + 1) // 2 < n:
            break  # parts part, part-1, ..., 1 cannot reach n: prune
        for rest in distinct_parts(n - part, part - 1):
            yield [part] + rest
