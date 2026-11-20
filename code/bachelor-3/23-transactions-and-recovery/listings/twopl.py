"""twopl.py -- strict two-phase locking with a deterministic scheduler. A read takes
a shared lock, a write an exclusive one (upgrading a shared lock held alone); all
locks are released at commit. A blocked transaction waits; a cycle in the wait-for
graph is a deadlock, broken by aborting its youngest transaction."""


class Scheduler:
    def __init__(self, programs, verbose=True):
        self.prog = {t: list(ops) for t, ops in programs.items()}  # t: [(op, item)]
        self.locks = {}  # item -> {transaction: "S" or "X"}
        self.waits = {}  # waiting transaction -> the transactions it waits for
        self.done, self.aborted, self.log, self.verbose = [], [], [], verbose
        self.history = []  # the operations granted, in order: (t, op, item)

    def say(self, text):
        self.log.append(text)
        if self.verbose:
            print(text)

    def blockers(self, t, op, item):
        held = self.locks.get(item, {})
        if op == "R":
            return {u for u, m in held.items() if u != t and m == "X"}
        return {u for u in held if u != t}

    def step(self, t):
        """Try t's next operation; return False if it must wait."""
        op, item = self.prog[t][0]
        if op == "C":
            for held in self.locks.values():
                held.pop(t, None)
            self.prog[t].pop(0)
            self.done.append(t)
            self.say(f"T{t} commits and releases its locks")
            return True
        others = self.blockers(t, op, item)
        if others:
            new = t not in self.waits
            self.waits[t] = others
            self.on_wait(t)  # may abort t, or another transaction
            if new and t in self.waits:
                names = ", ".join(f"T{u}" for u in sorted(others))
                self.say(f"T{t} {op}({item}) waits for {names}")
            return False
        self.waits.pop(t, None)
        mode = "X" if op == "W" else self.locks.get(item, {}).get(t, "S")
        self.locks.setdefault(item, {})[t] = mode
        self.prog[t].pop(0)
        self.history.append((t, op, item))
        self.say(f"T{t} {op}({item}) with an {mode} lock")
        return True

    def on_wait(self, t):
        """Deadlock detection: follow wait-for edges from t back to t."""
        path, frontier = {t: None}, [t]
        while frontier:
            u = frontier.pop()
            for v in self.waits.get(u, ()):
                if v == t:
                    cycle = [u]
                    while path[cycle[-1]] is not None:
                        cycle.append(path[cycle[-1]])
                    ring = " waits for ".join(f"T{x}" for x in cycle[::-1] + [t])
                    self.abort(max(cycle), f"deadlock, {ring}")
                    return
                if v not in path:
                    path[v] = u
                    frontier.append(v)

    def abort(self, t, why):
        for held in self.locks.values():
            held.pop(t, None)
        self.prog[t], self.waits = (
            [],
            {u: w - {t} for u, w in self.waits.items() if u != t},
        )
        self.aborted.append(t)
        self.say(f"{why}: abort T{t}")

    def run(self, order):
        """Offer steps in the given order (a waiting transaction lets its turn pass),
        then to the first transaction that is not waiting, until all are done."""
        queue = list(order)
        while any(self.prog.values()):
            ready = [
                u for u in sorted(self.prog) if self.prog[u] and u not in self.waits
            ]
            t = queue.pop(0) if queue else ready[0]
            if self.prog[t]:
                self.step(t)
                for u in sorted(self.waits):  # retry the waiters: a release may
                    if u in self.waits:  # unblock one, a new lock may close a cycle
                        self.step(u)
        return self


def program(text):
    """'R(A) W(A) C' -> [('R', 'A'), ('W', 'A'), ('C', None)]"""
    return [
        (op[0], op[2:-1] or None) if "(" in op else (op, None) for op in text.split()
    ]


if __name__ == "__main__":
    cases = {
        "no conflict": ({1: "R(A) W(A) C", 2: "R(B) W(B) C"}, [1, 2, 1, 2, 1, 2]),
        "blocked": (
            {1: "R(A) W(A) R(B) W(B) C", 2: "R(A) W(A) C"},
            [1, 1, 2, 1, 1, 1, 2],
        ),
        "deadlock": ({1: "R(A) W(B) C", 2: "R(B) W(A) C"}, [1, 2, 1, 2]),
    }
    for name, (progs, order) in cases.items():
        print(f"-- {name}: order {' '.join(f'T{t}' for t in order)}")
        Scheduler({t: program(p) for t, p in progs.items()}).run(order)
