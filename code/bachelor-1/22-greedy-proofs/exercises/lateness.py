"""lateness.py: tasks (length, deadline) on one machine, all to be done: the order that
minimises the largest lateness is by earliest deadline."""

from itertools import permutations


def max_lateness(order):
    t, worst = 0, 0
    for length, deadline in order:
        t += length
        worst = max(worst, t - deadline)
    return worst


def earliest_deadline(tasks):
    return sorted(tasks, key=lambda t: t[1])


def brute(tasks):
    return min(max_lateness(p) for p in permutations(tasks))
