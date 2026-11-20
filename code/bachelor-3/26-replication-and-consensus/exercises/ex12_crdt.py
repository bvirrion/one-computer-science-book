"""Exercise 12: a page-view counter replicated on three replicas that accept writes
alone and exchange their state later. With a last-writer-wins register, each replica
writes value + 1 with a timestamp; with a grow-only counter, each replica counts its
own increments and a merge takes the maximum per replica."""

import random


class LWWRegister:
    def __init__(self):
        self.value, self.stamp = 0, (0, "")

    def increment(self, time, replica):
        self.value, self.stamp = self.value + 1, (time, replica)  # read, add 1, write

    def merge(self, other):
        if other.stamp > self.stamp:
            self.value, self.stamp = other.value, other.stamp


class GCounter:
    def __init__(self):
        self.counts = {}

    def increment(self, time, replica):
        self.counts[replica] = self.counts.get(replica, 0) + 1

    def merge(self, other):
        for r, c in other.counts.items():
            self.counts[r] = max(self.counts.get(r, 0), c)

    @property
    def value(self):
        return sum(self.counts.values())


def simulate(kind, seed, steps=300):
    """Random increments and one-way merges, then a full exchange."""
    rng = random.Random(seed)
    names = ["R1", "R2", "R3"]
    reps, made = {n: kind() for n in names}, 0
    for t in range(steps):
        a = rng.choice(names)
        if rng.random() < 0.7:
            reps[a].increment(t, a)
            made += 1
        else:
            reps[a].merge(reps[rng.choice(names)])
    for a in names:  # finally everyone hears from everyone
        for b in names:
            reps[a].merge(reps[b])
    return made, [reps[n].value for n in names]


if __name__ == "__main__":
    for kind in (LWWRegister, GCounter):
        made, seen = simulate(kind, 12)
        print(f"{kind.__name__:<12} {made} increments made, replicas show {seen}")
