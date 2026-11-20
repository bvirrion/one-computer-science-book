"""mvcc.py -- multiversion concurrency control with snapshot isolation. Each item
keeps its committed versions with their commit timestamps; a transaction reads the
newest version committed before it began, and of two concurrent transactions that
write the same item the second to commit aborts. With ssi=True a transaction also
aborts at commit when it has rw-antidependencies both in and out among concurrent
transactions: the dangerous structure of serialisable snapshot isolation."""


class Store:
    def __init__(self, data, ssi=False):
        self.versions = {k: [(0, v)] for k, v in data.items()}
        self.clock, self.ssi, self.txns = 0, ssi, []

    def begin(self, name):
        t = Txn(self, name, self.clock)
        self.txns.append(t)
        return t

    def latest(self):
        return {k: vs[-1][1] for k, vs in self.versions.items()}


class Txn:
    def __init__(self, store, name, start):
        self.store, self.name, self.start = store, name, start
        self.reads, self.writes, self.commit_ts, self.state = set(), {}, None, "active"

    def read(self, item):
        self.reads.add(item)
        if item in self.writes:
            return self.writes[item]
        return [v for ts, v in self.store.versions[item] if ts <= self.start][-1]

    def write(self, item, value):
        self.writes[item] = value

    def concurrent(self):
        return [
            u
            for u in self.store.txns
            if u is not self
            and u.state != "aborted"
            and (u.commit_ts is None or u.commit_ts > self.start)
        ]

    def commit(self):
        s = self.store
        for item in self.writes:  # first committer wins
            if s.versions[item][-1][0] > self.start:
                return self.abort(f"{item} was changed by a concurrent commit")
        if s.ssi:
            others = self.concurrent()
            out_ = [u for u in others if self.reads & set(u.writes)]
            in_ = [u for u in others if u.reads & set(self.writes)]
            if out_ and in_:
                return self.abort("dangerous structure: rw-antidependencies in and out")
        s.clock += 1
        self.commit_ts, self.state = s.clock, "committed"
        for item, value in self.writes.items():
            s.versions[item].append((s.clock, value))
        return f"{self.name} commits at {s.clock}"

    def abort(self, why):
        self.state = "aborted"
        return f"{self.name} aborts: {why}"


def doctors(ssi):
    """Alice and Bob are on call; each wants to go off if someone else stays on."""
    s = Store({"alice": True, "bob": True}, ssi)
    t1, t2 = s.begin("T1"), s.begin("T2")
    for t, me in ((t1, "alice"), (t2, "bob")):
        on_call = t.read("alice") + t.read("bob")
        print(f"{t.name} sees {on_call} on call")
        if on_call >= 2:
            t.write(me, False)
    print(t1.commit())
    print(t2.commit())
    print("on call now:", [k for k, v in s.latest().items() if v] or "nobody")


if __name__ == "__main__":
    print("-- lost update under snapshot isolation")
    s = Store({"copies": 3})
    t1, t2 = s.begin("T1"), s.begin("T2")
    t1.write("copies", t1.read("copies") - 1)
    t2.write("copies", t2.read("copies") - 1)
    print(t1.commit())
    print(t2.commit())
    print("copies:", s.latest()["copies"])
    print("-- write skew under snapshot isolation")
    doctors(ssi=False)
    print("-- the same under serialisable snapshot isolation")
    doctors(ssi=True)
