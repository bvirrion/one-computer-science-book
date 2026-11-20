"""Exercise 6: causal broadcast on netsim. Every process broadcasts to all the others;
a message carries the sender's vector of broadcasts delivered, and a receiver holds it
back until every message it depends on has been delivered."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from netsim import Net, Process  # noqa: E402


class Member(Process):
    def __init__(self, name, names, to_send):
        super().__init__(name)
        self.names, self.i = names, names.index(name)
        self.v = [0] * len(names)  # v[k]: broadcasts of member k delivered here
        self.pending, self.delivered, self.to_send = [], [], to_send

    def on_start(self):
        if self.to_send:
            self.set_timer(1, "say")

    def on_timer(self, what):
        self.v[self.i] += 1
        msg = (self.name, self.v.copy(), f"{self.name}#{self.v[self.i]}")
        self.delivered.append(msg[2])  # a member delivers its own broadcast at once
        for p in self.names:
            if p != self.name:
                self.send(p, msg)
        self.to_send -= 1
        if self.to_send > 0:
            self.set_timer(self.net.rng.randint(1, 3), "say")

    def deliverable(self, msg):
        j, vm = self.names.index(msg[0]), msg[1]
        return vm[j] == self.v[j] + 1 and all(
            vm[k] <= self.v[k] for k in range(len(vm)) if k != j
        )

    def on_message(self, src, msg):
        self.pending.append(msg)
        progress = True
        while progress:
            progress = False
            for m in list(self.pending):
                if self.deliverable(m):
                    self.pending.remove(m)
                    self.v[self.names.index(m[0])] += 1
                    self.delivered.append(m[2])
                    progress = True


class Replier(Member):
    """Answers P1's first broadcast at once: a reply caused by what it received."""

    def on_message(self, src, msg):
        before = len(self.delivered)
        super().on_message(src, msg)
        if any(m == "P1#1" for m in self.delivered[before:]):
            self.on_timer("say")


def run(seed, causal=True):
    names = ["P1", "P2", "P3"]
    net = Net(seed=seed, delay=(1, 12), fifo=False)
    members = [Member("P1", names, 3), Replier("P2", names, 0), Member("P3", names, 0)]
    if not causal:
        for m in members:
            m.deliverable = lambda msg: True
    net.add(*members)
    net.run()
    return {m.name: m.delivered for m in members}


def violates(order):
    """A message delivered before one it causally depends on."""
    return order.index("P2#1") < order.index("P1#1") if "P2#1" in order else False


if __name__ == "__main__":
    for causal in (False, True):
        bad = sum(violates(run(seed, causal)["P3"]) for seed in range(200))
        print(f"causal={causal}: P3 sees the reply first in {bad} of 200 runs")
