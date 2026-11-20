"""netsim.py -- a deterministic discrete-event simulator of processes that exchange
messages. Time is an integer; each message takes a random delay from a seeded
generator and may be lost; channels are FIFO unless told otherwise. Processes can
crash, recover, and be cut off from each other by a partition. Every event is
recorded in net.log, so a run prints the same transcript every time."""

import heapq
import random


class Process:
    """Subclass and override on_start, on_message and on_timer."""

    def __init__(self, name):
        self.name, self.net, self.up = name, None, True

    def send(self, dst, msg):
        self.net.send(self.name, dst, msg)

    def set_timer(self, delay, what):
        self.net.timer(self.name, delay, what)

    def on_start(self):
        pass

    def on_message(self, src, msg):
        pass

    def on_timer(self, what):
        pass


class Net:
    def __init__(self, seed=0, delay=(1, 5), loss=0.0, fifo=True):
        self.rng = random.Random(seed)
        self.delay, self.loss, self.fifo = delay, loss, fifo
        self.procs, self.queue, self.now, self.seq = {}, [], 0, 0
        self.last = {}  # (src, dst) -> last delivery time scheduled on that channel
        self.cut, self.log = set(), []  # cut: pairs that cannot communicate

    def add(self, *procs):
        for p in procs:
            p.net, self.procs[p.name] = self, p

    def at(self, time, action):
        """Schedule a function to run at a time (a crash, a partition, a request)."""
        self.push(time, ("call", action))

    def push(self, time, event):
        self.seq += 1
        heapq.heappush(self.queue, (time, self.seq, event))

    def send(self, src, dst, msg):
        if self.rng.random() < self.loss or (src, dst) in self.cut:
            self.log.append((self.now, "lost", src, dst, msg))
            return
        t = self.now + self.rng.randint(*self.delay)
        if self.fifo:
            t = max(t, self.last.get((src, dst), 0))
            self.last[(src, dst)] = t
        self.log.append((self.now, "send", src, dst, msg))
        self.push(t, ("deliver", src, dst, msg))

    def timer(self, name, delay, what):
        self.push(self.now + delay, ("timer", name, what))

    def crash(self, name):
        self.procs[name].up = False
        self.log.append((self.now, "crash", name, None, None))

    def recover(self, name):
        p = self.procs[name]
        p.up = True
        self.log.append((self.now, "recover", name, None, None))
        if hasattr(p, "on_recover"):
            p.on_recover()

    def partition(self, *groups):
        """Cut every pair of processes in different groups; partition() heals."""
        self.cut = {
            (a, b) for g in groups for h in groups if g is not h for a in g for b in h
        }
        self.log.append(
            (self.now, "partition", None, None, [sorted(g) for g in groups])
        )

    def run(self, until=10**9):
        for p in self.procs.values():
            p.on_start()
        while self.queue and self.queue[0][0] <= until:
            self.now, _, ev = heapq.heappop(self.queue)
            if ev[0] == "call":
                ev[1]()
            elif ev[0] == "deliver":
                _, src, dst, msg = ev
                if self.procs[dst].up and (src, dst) not in self.cut:
                    self.log.append((self.now, "recv", src, dst, msg))
                    self.procs[dst].on_message(src, msg)
                else:
                    self.log.append((self.now, "dropped", src, dst, msg))
            elif self.procs[ev[1]].up:
                self.procs[ev[1]].on_timer(ev[2])
        return self
