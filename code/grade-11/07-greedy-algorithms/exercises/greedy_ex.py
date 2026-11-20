"""Exercises of the chapter on greedy algorithms."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from change_exhaustive import fewest  # noqa: E402


def greedy_change(amount, coins):                 # exercise 5
    given = []
    for c in sorted(coins, reverse=True):
        k, amount = divmod(amount, c)
        given += [c] * k
    return given


def by_start(requests):                           # exercise 6: the wrong order
    chosen, free_from = [], 0
    for name, start, end in sorted(requests, key=lambda r: r[1]):
        if start >= free_from:
            chosen.append(name)
            free_from = end
    return chosen


def max_activities(requests):                     # exercise 7
    chosen, free_from = [], 0
    for name, start, end in sorted(requests, key=lambda r: r[2]):
        if start >= free_from:
            chosen.append(name)
            free_from = end
    return chosen


def greedy_by_value(goods, capacity):             # exercise 9: the wrong key
    value = 0
    for _, kg, worth in sorted(goods, key=lambda g: g[2], reverse=True):
        take = min(kg, capacity)
        value += worth * take / kg
        capacity -= take
    return value


def is_canonical_upto(coins, m):                  # exercise 11
    return all(len(greedy_change(a, coins)) == fewest(a, sorted(coins))[0]
               for a in range(1, m + 1))


def rooms_needed(requests):                       # exercise 14
    """Give each booking, by start time, the first room free; return the rooms used."""
    rooms = []                                    # rooms[i]: the hour room i is free
    for _, start, end in sorted(requests, key=lambda r: r[1]):
        for i, free in enumerate(rooms):
            if free <= start:
                rooms[i] = end
                break
        else:
            rooms.append(end)
    return len(rooms)


def shortest_first(requests):                     # exercise 15
    chosen = []
    for r in sorted(requests, key=lambda r: r[2] - r[1]):
        if all(r[2] <= c[1] or c[2] <= r[1] for c in chosen):
            chosen.append(r)
    return [name for name, _, _ in chosen]


if __name__ == "__main__":
    print(greedy_change(87, [1, 2, 5, 10, 20, 50]), fewest(20, [1, 2, 5]))
    long_first = [("L", 8, 20), ("x", 9, 10), ("y", 10, 11), ("z", 11, 12)]
    print(by_start(long_first), max_activities(long_first))
    print(is_canonical_upto([1, 3, 4], 10), is_canonical_upto([1, 2, 5], 10))
    print(shortest_first([("P", 8, 12), ("S", 11, 13), ("Q", 12, 16)]))
