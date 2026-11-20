"""additive_count.py: words of length 4 over a..z, grouped by their additive hash."""

from collections import Counter
from itertools import product


def sums(length=4):
    return Counter(sum(map(ord, w)) for w in product("abcdefghijklmnopqrstuvwxyz",
                                                      repeat=length))


def most_common(length=4):
    value, count = sums(length).most_common(1)[0]
    return value, count, len(sums(length))
