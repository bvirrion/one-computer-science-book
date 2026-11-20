"""Exercise 13: count the 1 bits of a number in two ways, counting the loop turns."""


def popcount_shift(x):
    """Return (number of 1 bits of x >= 0, loop turns), bit by bit."""
    count = turns = 0
    while x != 0:
        count += x & 1
        x = x >> 1
        turns += 1
    return count, turns


def popcount(x):
    """Return (number of 1 bits, loop turns); x & (x - 1) clears the lowest 1."""
    count = 0
    while x != 0:
        x = x & (x - 1)
        count += 1
    return count, count
