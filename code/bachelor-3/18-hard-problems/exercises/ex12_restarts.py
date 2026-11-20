"""ex12_restarts.py -- CDCL with restarts: after a number of conflicts that follows the
sequence 1, 1, 2, 1, 1, 2, 4, 1, ... times a unit, drop every decision and keep the
learned clauses."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from cdcl import CDCL  # noqa: E402


def reluctant(i):
    """The i-th term (from 1): 2^(k-1) when i = 2^k - 1, else term i - 2^(k-1) + 1."""
    k = 1
    while (1 << k) - 1 < i:
        k += 1
    if i == (1 << k) - 1:
        return 1 << (k - 1)
    return reluctant(i - (1 << (k - 1)) + 1)


class Restarting(CDCL):
    def __init__(self, clauses, n, unit=16):
        super().__init__(clauses, n)
        self.unit, self.run, self.count = unit, 1, 0
        self.stats["restarts"] = 0

    def restart_now(self):
        self.count += 1
        if self.count < self.unit * reluctant(self.run):
            return False
        self.run, self.count = self.run + 1, 0
        self.stats["restarts"] += 1
        return True


if __name__ == "__main__":
    import random

    from sat_compare import random_3sat
    rng = random.Random(18)
    for n in (60, 80, 100):
        clauses, _ = random_3sat(n, 4.26, rng)
        a = CDCL(clauses, n).solve()[1]
        b = Restarting(clauses, n).solve()[1]
        print(n, a["conflicts"], b["conflicts"], b["restarts"])
