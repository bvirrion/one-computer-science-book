"""cdcl.py -- a conflict-driven clause-learning SAT solver: two watched literals per
clause, conflict analysis to the first unique implication point, a learned clause, and
a backjump. Literals are +i and -i; returns (assignment or None, statistics)."""


class CDCL:
    def __init__(self, clauses, n):
        self.n, self.clauses = n, []
        self.value, self.level, self.reason = {}, {}, {}
        self.trail, self.head, self.watches, self.limits = [], 0, {}, []
        self.activity = {v: 0.0 for v in range(1, n + 1)}
        self.stats = {"decisions": 0, "conflicts": 0, "learned": 0}
        self.unsat = False
        for c in clauses:
            c = list(dict.fromkeys(c))  # drop repeated literals
            if not c:
                self.unsat = True
            elif len(c) == 1:
                if not self.assign(c[0], None) and self.true(-c[0]):
                    self.unsat = True
            else:
                self.add(c)

    def true(self, lit):
        return self.value.get(abs(lit)) == (lit > 0)

    def false(self, lit):
        return self.value.get(abs(lit)) == (lit < 0)

    def assign(self, lit, reason):
        if abs(lit) in self.value:
            return False
        self.value[abs(lit)] = lit > 0
        self.level[abs(lit)] = self.decision_level()
        self.reason[abs(lit)] = reason  # None for a decision, else a clause index
        self.trail.append(lit)
        return True

    def decision_level(self):
        return len(self.limits)  # limits[d] = length of the trail before decision d

    def add(self, c):
        self.clauses.append(c)
        for lit in c[:2]:  # watch the first two literals
            self.watches.setdefault(lit, []).append(len(self.clauses) - 1)
        return len(self.clauses) - 1

    def propagate(self):
        """Unit propagation through the watches; returns a falsified clause or None."""
        while self.head < len(self.trail):
            falsified = -self.trail[self.head]
            self.head += 1
            watching = self.watches.get(falsified, [])
            self.watches[falsified] = []
            for k, ci in enumerate(watching):
                c = self.clauses[ci]
                if c[0] == falsified:
                    c[0], c[1] = c[1], c[0]
                if self.true(c[0]):
                    self.watches[falsified].append(ci)
                    continue
                for j in range(2, len(c)):  # look for another literal to watch
                    if not self.false(c[j]):
                        c[1], c[j] = c[j], c[1]
                        self.watches.setdefault(c[1], []).append(ci)
                        break
                else:
                    self.watches[falsified].append(ci)
                    if self.false(c[0]):  # every literal false: a conflict
                        self.watches[falsified] += watching[k + 1:]
                        return c
                    self.assign(c[0], ci)  # unit: c[0] is implied
        return None

    def analyse(self, conflict):
        """First UIP: resolve the conflict clause with the reasons of its literals of
        the current level, latest first, until one literal of that level is left."""
        level, seen, learned, count = self.decision_level(), set(), [], 0
        clause, i = conflict, len(self.trail) - 1
        while True:
            for lit in clause:
                v = abs(lit)
                if v in seen or self.level[v] == 0:
                    continue
                seen.add(v)
                self.activity[v] += 1
                if self.level[v] == level:
                    count += 1  # still to be resolved away
                else:
                    learned.append(lit)
            while abs(self.trail[i]) not in seen:
                i -= 1
            uip = self.trail[i]
            i, count = i - 1, count - 1
            if count == 0:
                break
            clause = [x for x in self.clauses[self.reason[abs(uip)]] if x != uip]
        learned.insert(0, -uip)  # the learned clause: not uip, or the earlier literals
        back = max((self.level[abs(x)] for x in learned[1:]), default=0)
        return learned, back

    def restart_now(self):
        """No restarts here; exercise 12 overrides this."""
        return False

    def backjump(self, level):
        """Undo every assignment made after decision level `level`."""
        for lit in self.trail[self.limits[level]:]:
            del self.value[abs(lit)], self.level[abs(lit)], self.reason[abs(lit)]
        del self.trail[self.limits[level]:]
        del self.limits[level:]
        self.head = len(self.trail)

    def solve(self):
        if self.unsat or self.propagate() is not None:
            return None, self.stats
        while True:
            conflict = self.propagate()
            if conflict is not None:
                self.stats["conflicts"] += 1
                if self.decision_level() == 0:
                    return None, self.stats
                learned, back = self.analyse(conflict)
                self.backjump(back)
                # watch the asserting literal and the latest of the others
                learned[1:] = sorted(learned[1:], key=lambda x: -self.level[abs(x)])
                ci = self.add(learned) if len(learned) > 1 else None
                self.assign(learned[0], ci)
                self.stats["learned"] += 1
                if self.restart_now() and self.limits:
                    self.backjump(0)  # keep the learned clauses, forget the decisions
                continue
            free = [v for v in range(1, self.n + 1) if v not in self.value]
            if not free:
                return dict(self.value), self.stats
            v = max(free, key=lambda v: (self.activity[v], -v))  # most active variable
            self.stats["decisions"] += 1
            self.limits.append(len(self.trail))
            self.assign(-v, None)  # try false first
