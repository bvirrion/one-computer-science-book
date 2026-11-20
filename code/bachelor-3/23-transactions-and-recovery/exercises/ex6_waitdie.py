"""ex6_waitdie.py -- wait-die in twopl's lock manager. A transaction's number is its
timestamp: the smaller, the older. An older transaction asking for a lock held by
younger ones waits; a younger one asking for a lock an older one holds dies (aborts)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from doctors import orders  # noqa: E402
from twopl import Scheduler, program  # noqa: E402


class WaitDie(Scheduler):
    def on_wait(self, t):
        if any(u < t for u in self.waits[t]):  # t is younger than a holder: it dies
            op, item = self.prog[t][0]
            self.abort(t, f"T{t} {op}({item}) dies, younger than T{min(self.waits[t])}")


if __name__ == "__main__":
    progs = {1: "R(A) W(B) C", 2: "R(B) W(A) C"}
    for order in ([1, 2, 1, 2], [2, 1, 2, 1]):
        print(f"-- order {' '.join(f'T{t}' for t in order)}")
        WaitDie({t: program(p) for t, p in progs.items()}).run(order)
    doc = {1: "R(A) R(B) W(A) C", 2: "R(A) R(B) W(B) C"}
    died = sum(
        bool(
            WaitDie({t: program(p) for t, p in doc.items()}, verbose=False)
            .run(o)
            .aborted
        )
        for o in orders()
    )
    print(f"doctors: {died} of 70 orders abort a transaction under wait-die")
