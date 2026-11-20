"""channel.py: a discrete-event simulator and a seeded, unreliable one-way link."""
import heapq
import random


class Sim:
    def __init__(self):
        self.now, self.queue, self.count = 0.0, [], 0

    def at(self, t, fn, *args):
        self.count += 1                          # ties run in the order scheduled
        heapq.heappush(self.queue, (t, self.count, fn, args))

    def run(self, until=float("inf")):
        while self.queue and self.queue[0][0] <= until:
            self.now, _, fn, args = heapq.heappop(self.queue)
            fn(*args)


class Link:
    """Delay, transmission time; seeded loss, duplication and jitter (reordering)."""

    def __init__(self, sim, deliver, delay=50.0, tx=1.0, loss=0.0, dup=0.0, jitter=0.0,
                 seed=0):
        self.sim, self.deliver = sim, deliver
        self.delay, self.tx, self.jitter = delay, tx, jitter
        self.loss, self.dup = loss, dup
        self.rng = random.Random(seed)
        self.busy_until, self.sent, self.lost = 0.0, 0, 0

    def send(self, packet):
        start = max(self.sim.now, self.busy_until)
        self.busy_until = start + self.tx        # one packet on the wire at a time
        self.sent += 1
        if self.rng.random() < self.loss:
            self.lost += 1
            return
        copies = 2 if self.rng.random() < self.dup else 1
        for _ in range(copies):
            t = self.busy_until + self.delay + self.rng.uniform(0, self.jitter)
            self.sim.at(t, self.deliver, packet)
