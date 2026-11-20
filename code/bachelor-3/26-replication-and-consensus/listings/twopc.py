"""twopc.py -- two-phase commit on netsim: a coordinator and three participants.
Each participant writes its vote to its log before sending it, and the coordinator
writes its decision before sending it. Three runs: all vote yes; one votes no; all
vote yes and the coordinator crashes after writing its decision, before sending it."""

from raft import Net, Process

PARTS = ["P1", "P2", "P3"]


class Coordinator(Process):
    def __init__(self, crash_at_decision=False):
        super().__init__("C")
        self.crash_at_decision, self.votes, self.decision = crash_at_decision, {}, None

    def on_start(self):
        self.net.notes.append(f"t={self.net.now:>3} C: prepare?")
        for p in PARTS:
            self.send(p, ("prepare?", None))

    def on_message(self, src, msg):
        if msg[0] == "vote":
            self.votes[src] = msg[1]
            if len(self.votes) == len(PARTS):
                self.decision = "commit" if all(self.votes.values()) else "abort"
                self.net.notes.append(f"t={self.net.now:>3} C: logs {self.decision}")
                if self.crash_at_decision:
                    self.net.crash("C")
                    self.net.notes.append(f"t={self.net.now:>3} C crashes")
                    return
                self.announce()
        elif msg[0] == "decision?" and self.decision:
            self.send(src, ("decision", self.decision))

    def announce(self):
        for p in PARTS:
            self.send(p, ("decision", self.decision))

    def on_recover(self):
        self.net.notes.append(f"t={self.net.now:>3} C restarts, reads {self.decision}")
        self.announce()


class Participant(Process):
    def __init__(self, name, vote):
        super().__init__(name)
        self.vote, self.decision, self.since, self.asked = vote, None, None, 0

    def on_message(self, src, msg):
        kind, value = msg
        if kind == "prepare?":
            self.since = self.net.now  # the vote is logged, then sent
            self.send("C", ("vote", self.vote))
            if self.vote:
                self.set_timer(20, "ask")
            else:
                self.finish("abort")  # a no can abort at once
        elif kind == "decision" and self.decision is None:
            self.finish(value)
        elif kind == "decision?" and self.decision:
            self.send(src, ("decision", self.decision))

    def finish(self, decision):
        self.decision = decision
        held = self.net.now - self.since
        self.net.notes.append(
            f"t={self.net.now:>3} {self.name}: {decision}, "
            f"locks held {held}, asked {self.asked} times"
        )

    def on_timer(self, what):
        if self.decision is None:  # voted yes: may neither commit nor abort alone
            self.asked += 1
            for p in ["C"] + [q for q in PARTS if q != self.name]:
                self.send(p, ("decision?", None))
            self.set_timer(20, "ask")


def run(votes, crash=False):
    net = Net(seed=3)
    net.notes = []
    net.add(Coordinator(crash), *(Participant(p, v) for p, v in zip(PARTS, votes)))
    if crash:
        net.at(300, lambda: net.recover("C"))
    net.run(until=400)
    return net


if __name__ == "__main__":
    for title, votes, crash in [
        ("all vote yes", (1, 1, 1), False),
        ("P2 votes no", (1, 0, 1), False),
        ("the coordinator crashes", (1, 1, 1), True),
    ]:
        print(f"-- {title}")
        print("\n".join(run(votes, crash).notes))
