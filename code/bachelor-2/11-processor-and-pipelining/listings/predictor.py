"""predictor.py: branch predictors, each a predict(pc) and an update(pc, taken)."""


class NotTaken:
    """Static prediction: every branch falls through."""
    name = "not taken"

    def predict(self, pc):
        return False

    def update(self, pc, taken):
        pass


class OneBit:
    """One bit per branch: predict what the branch did last time."""
    name = "one-bit"

    def __init__(self):
        self.last = {}

    def predict(self, pc):
        return self.last.get(pc, False)

    def update(self, pc, taken):
        self.last[pc] = taken


class TwoBit:
    """A two-bit saturating counter per branch: 0, 1 predict not taken; 2, 3 taken."""
    name = "two-bit"

    def __init__(self, start=1):
        self.start = start
        self.counter = {}

    def predict(self, pc):
        return self.counter.get(pc, self.start) >= 2

    def update(self, pc, taken):
        c = self.counter.get(pc, self.start)
        self.counter[pc] = min(c + 1, 3) if taken else max(c - 1, 0)


def mispredictions(branches, predictor):
    """branches: (pc, taken) pairs in execution order. Returns the misses."""
    wrong = 0
    for pc, taken in branches:
        wrong += predictor.predict(pc) != taken
        predictor.update(pc, taken)
    return wrong
