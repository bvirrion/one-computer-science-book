"""stairs.py: the number of ways to climb n stairs with steps of the given sizes."""


def climbs(n, steps):
    ways = [1] + [0] * n  # ways[k]: ordered sequences of steps summing to k
    for k in range(1, n + 1):
        ways[k] = sum(ways[k - s] for s in steps if s <= k)
    return ways[n]
