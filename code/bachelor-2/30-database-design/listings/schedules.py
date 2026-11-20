"""schedules.py: a small simulator of interleaved transactions under three ways of
answering a read: the latest write even uncommitted, the latest committed value, or
a snapshot taken when the transaction starts. Each schedule stages one anomaly."""


class Db:
    def __init__(self, data, policy):
        self.committed, self.policy = dict(data), policy
        self.writes, self.snap, self.start, self.version = {}, {}, {}, {}
        self.clock, self.log = 0, []  # log: uncommitted writes in time order

    def begin(self, t):
        if t not in self.writes:
            self.writes[t], self.snap[t] = {}, dict(self.committed)
            self.start[t] = self.clock

    def read(self, t, key):
        self.begin(t)
        if key in self.writes[t]:
            return self.writes[t][key]
        if self.policy == "uncommitted":
            for _, k, v in reversed(self.log):
                if k == key:
                    return v
        source = self.snap[t] if self.policy == "snapshot" else self.committed
        return source.get(key)

    def count(self, t, prefix):
        """How many keys with this prefix t can see: a query with a condition."""
        self.begin(t)
        keys = set(self.committed) | set(self.snap[t]) | {k for _, k, _ in self.log}
        return sum(1 for k in keys
                   if k.startswith(prefix) and self.read(t, k) is not None)

    def write(self, t, key, value):
        self.begin(t)
        self.writes[t][key] = value
        self.log.append((t, key, value))

    def commit(self, t):
        """Apply t's writes; under snapshot, refuse them if another transaction has
        committed one of the same keys since t started (first committer wins)."""
        self.begin(t)
        if self.policy == "snapshot" and any(
                self.version.get(k, -1) > self.start[t] for k in self.writes[t]):
            return self.abort(t, refused=True)
        self.clock += 1
        for k, v in self.writes[t].items():
            self.committed[k], self.version[k] = v, self.clock
        self.log = [e for e in self.log if e[0] != t]
        return True

    def abort(self, t, refused=False):
        self.begin(t)
        self.log = [e for e in self.log if e[0] != t]
        self.writes[t] = {}
        return not refused


def dirty_read(db):  # T2 reads a change that T1 then cancels
    db.write(1, "x", 0)
    seen = db.read(2, "x")
    db.abort(1)
    db.commit(2)
    return seen != db.committed["x"]


def non_repeatable_read(db):  # T1 reads x twice, T2 changes it in between
    first = db.read(1, "x")
    db.write(2, "x", 2)
    db.commit(2)
    return db.read(1, "x") != first


def phantom(db):  # T1 counts member 5's loans twice, T2 adds one in between
    first = db.count(1, "loan:")
    db.write(2, "loan:3", "member 5")
    db.commit(2)
    return db.count(1, "loan:") != first


def lost_update(db):  # both read x, both write what they read minus one
    a, b = db.read(1, "x"), db.read(2, "x")
    db.write(1, "x", a - 1)
    db.write(2, "x", b - 1)
    if not (db.commit(1) and db.commit(2)):
        return "refused"
    return db.committed["x"] != 1


def write_skew(db):  # the rule a + b >= 1; each checks it, each removes one copy
    s1 = db.read(1, "a") + db.read(1, "b")
    s2 = db.read(2, "a") + db.read(2, "b")
    if s1 >= 2:
        db.write(1, "a", 0)
    if s2 >= 2:
        db.write(2, "b", 0)
    if not (db.commit(1) and db.commit(2)):
        return "refused"
    return db.committed["a"] + db.committed["b"] < 1


CASES = [("dirty read", dirty_read, {"x": 3}),
         ("non-repeatable read", non_repeatable_read, {"x": 3}),
         ("phantom", phantom, {"loan:1": "member 5", "loan:2": "member 5"}),
         ("lost update", lost_update, {"x": 3}),
         ("write skew", write_skew, {"a": 1, "b": 1})]
POLICIES = ["uncommitted", "committed", "snapshot"]

if __name__ == "__main__":
    print(f"{'':20}" + "".join(f"{p:>14}" for p in POLICIES))
    for name, case, data in CASES:
        cells = []
        for p in POLICIES:
            r = case(Db(data, p))
            cells.append(r if isinstance(r, str) else "seen" if r else "-")
        print(f"{name:20}" + "".join(f"{c:>14}" for c in cells))
