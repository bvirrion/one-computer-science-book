"""snapshot.py -- five branches of a bank send each other money over FIFO channels;
1,000 transfers in all. During the run, 100 snapshots are taken by the Chandy-Lamport
algorithm, and 100 naive ones in which every branch just reports its balance when
asked. A correct snapshot must add up to the bank's total, 5,000."""

from netsim import Net, Process

N, TOTAL, TRANSFERS = 5, 5000, 1000


class Branch(Process):
    def __init__(self, name, bank):
        super().__init__(name)
        self.bank, self.balance, self.snaps = bank, TOTAL // N, {}

    def others(self):
        return [p for p in self.net.procs if p != self.name]

    def on_start(self):
        self.set_timer(self.net.rng.randint(1, 4), "transfer")

    def on_timer(self, what):
        if what[0] == "snapshot":  # this branch starts snapshot number what[1]
            self.record(what[1])
        elif self.bank.sent < TRANSFERS:  # a transfer to a random other branch
            if self.balance > 0:
                amount = self.net.rng.randint(1, min(100, self.balance))
                self.balance -= amount
                self.bank.sent += 1
                self.send(self.net.rng.choice(self.others()), ("money", amount))
            self.set_timer(self.net.rng.randint(1, 4), "transfer")

    def record(self, sid):
        """Record the balance, start recording every incoming channel, send markers."""
        self.snaps[sid] = {
            "balance": self.balance,
            "open": set(self.others()),
            "channels": 0,
        }
        for p in self.others():
            self.send(p, ("marker", sid))

    def on_message(self, src, msg):
        kind, x = msg
        if kind == "money":
            self.balance += x
            for s in self.snaps.values():  # money in transit when the snapshot passed
                if src in s["open"]:
                    s["channels"] += x
        elif kind == "marker":
            if x not in self.snaps:
                self.record(x)
            self.snaps[x]["open"].discard(src)  # the channel from src is now recorded
        elif kind == "report?":
            self.send(src, ("report", (x, self.balance)))
        elif kind == "report":
            self.bank.naive.setdefault(x[0], []).append(x[1])


class Bank:
    def __init__(self, seed, branch=Branch, fifo=True):
        self.sent, self.naive = 0, {}
        self.net = Net(seed=seed, delay=(1, 6), fifo=fifo)
        self.branches = [branch(f"B{i}", self) for i in range(1, N + 1)]
        self.net.add(*self.branches)
        # a Chandy-Lamport snapshot and a naive one every 5 ticks, from time 3
        for sid in range(100):
            b = self.branches[sid % N]
            self.net.at(5 * sid + 3, lambda b=b, sid=sid: b.on_timer(("snapshot", sid)))
            self.net.at(5 * sid + 3, lambda b=b, sid=sid: self.ask(b, sid))

    def ask(self, b, sid):
        self.naive[sid] = [b.balance]
        for p in b.others():
            b.send(p, ("report?", sid))

    def run(self):
        self.net.run()
        cl = [
            sum(b.snaps[s]["balance"] + b.snaps[s]["channels"] for b in self.branches)
            for s in range(100)
        ]
        naive = [sum(self.naive[s]) for s in range(100)]
        return cl, naive


if __name__ == "__main__":
    bank = Bank(seed=25)
    cl, naive = bank.run()
    end = sum(b.balance for b in bank.branches)
    print(f"{bank.sent} transfers; total at the end: {end}")
    for sid in (0, 50, 99):
        bal = [b.snaps[sid]["balance"] for b in bank.branches]
        transit = sum(b.snaps[sid]["channels"] for b in bank.branches)
        print(
            f"snapshot {sid:>2}: balances {bal}, in transit {transit}, "
            f"sum {sum(bal) + transit}"
        )
    markers = sum(
        1 for _, kind, _, _, m in bank.net.log if kind == "send" and m[0] == "marker"
    )
    print(
        f"Chandy-Lamport: {sum(t == TOTAL for t in cl)} of 100 snapshots "
        f"sum to {TOTAL}; {markers} markers sent"
    )
    wrong = [t for t in naive if t != TOTAL]
    print(f"naive: {len(wrong)} of 100 are wrong, from {min(naive)} to {max(naive)}")
