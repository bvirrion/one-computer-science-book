"""selective_repeat.py: a timer per packet; the receiver keeps early packets."""
from channel import Link, Sim


class Sender:
    def __init__(self, sim, data, k, window, timeout):
        assert window <= 2 ** (k - 1), "selective repeat needs W <= 2^(k-1)"
        self.sim, self.data, self.timeout = sim, data, timeout
        self.M, self.W = 2**k, window
        self.base = self.next = 0
        self.acked, self.link = set(), None

    def fill(self):
        while self.next < len(self.data) and self.next < self.base + self.W:
            self.send(self.next)
            self.next += 1

    def send(self, i):
        self.link.send((i % self.M, self.data[i]))
        self.sim.at(self.sim.now + self.timeout, self.expire, i)

    def expire(self, i):
        if i >= self.base and i not in self.acked:
            self.send(i)                         # resend this packet only

    def on_ack(self, seq):
        offset = (seq - self.base) % self.M
        if offset < self.next - self.base:
            self.acked.add(self.base + offset)
            while self.base in self.acked:       # slide past every acked packet
                self.acked.discard(self.base)
                self.base += 1
            self.fill()


class Receiver:
    def __init__(self, k, window):
        self.M, self.W, self.base, self.buffer, self.out = 2**k, window, 0, {}, []
        self.link, self.clock, self.done = None, None, 0.0

    def on_packet(self, packet):
        seq, item = packet
        offset = (seq - self.base) % self.M
        if offset < self.W:                      # inside the window: keep it
            self.buffer.setdefault(self.base + offset, item)
            while self.base in self.buffer:      # deliver what is now in order
                self.out.append(self.buffer.pop(self.base))
                self.base += 1
                self.done = self.clock.now
            self.link.send(seq)
        elif offset >= self.M - self.W:          # the window before: already delivered
            self.link.send(seq)                  # its ack was lost; ack it again


def transfer(data, k=4, window=8, timeout=150.0, **link):
    sim = Sim()
    s, r = Sender(sim, data, k, window, timeout), Receiver(k, window)
    r.clock = sim
    s.link = Link(sim, r.on_packet, **link)
    r.link = Link(sim, s.on_ack, **dict(link, seed=link.get("seed", 0) + 1))
    s.fill()
    sim.run()
    return r.out, r.done, s.link


if __name__ == "__main__":
    data = list(range(5000))
    print("loss 5 %, duplicates 2 %, W 31:")
    out, t, link = transfer(data, k=6, window=31, loss=0.05, dup=0.02, seed=3)
    print(f"  intact {out == data}, {link.sent} sent for {len(data)}, {t / 1000:.1f} s")
