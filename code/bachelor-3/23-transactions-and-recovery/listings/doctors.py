"""doctors.py -- the clinic's rule: at least one of Alice (A) and Bob (B) on call.
T1 lets Alice go off and T2 lets Bob go off, each in four steps: read A, read B,
write its own row off if both were on call, commit. Every one of the C(8, 4)
interleavings is run under snapshot isolation, under snapshot isolation with the
conflict materialised, under serialisable snapshot isolation and under strict 2PL."""

from itertools import combinations

from mvcc import Store
from twopl import Scheduler, program


def orders():
    for slots in combinations(range(8), 4):
        yield [1 if k in slots else 2 for k in range(8)]


def run_mvcc(order, ssi=False, materialise=False):
    s = Store({"A": True, "B": True, "duty": 0}, ssi)
    txns, step, seen = {}, {1: 0, 2: 0}, {1: 0, 2: 0}
    for t in order:
        if step[t] == 0:
            txns[t] = s.begin(f"T{t}")
        tx, k = txns[t], step[t]
        if tx.state == "active":
            if k < 2:
                seen[t] += tx.read("AB"[k])
            elif k == 2 and seen[t] == 2:
                tx.write("AB"[t - 1], False)
                if materialise:  # both write one shared row: a write-write conflict
                    tx.write("duty", t)
            elif k == 3:
                tx.commit()
        step[t] += 1
    aborts = sum(tx.state == "aborted" for tx in txns.values())
    return not (s.latest()["A"] or s.latest()["B"]), aborts


class Doctors(Scheduler):
    def __init__(self):
        super().__init__(
            {1: program("R(A) R(B) W(A) C"), 2: program("R(A) R(B) W(B) C")},
            verbose=False,
        )
        self.values, self.seen, self.pending = {"A": True, "B": True}, {1: 0, 2: 0}, {}

    def step(self, t):
        op, item = self.prog[t][0]
        if not super().step(t):
            return False
        if op == "R":
            self.seen[t] += self.values[item]
        elif op == "W" and self.seen[t] == 2:
            self.pending[t] = item
        elif op == "C" and t in self.pending:
            self.values[self.pending[t]] = False
        return True


def run_2pl(order):
    d = Doctors().run(order)
    return not any(d.values.values()), len(d.aborted)


if __name__ == "__main__":
    print("protocol                    nobody on call   aborts   (of 70 orders)")
    for name, run in (
        ("snapshot isolation", run_mvcc),
        ("SI, conflict materialised", lambda o: run_mvcc(o, materialise=True)),
        ("serialisable SI", lambda o: run_mvcc(o, ssi=True)),
        ("strict 2PL", run_2pl),
    ):
        results = [run(o) for o in orders()]
        broken = sum(b for b, _ in results)
        aborted = sum(a > 0 for _, a in results)
        print(f"{name:<27} {broken:>14} {aborted:>8}")
