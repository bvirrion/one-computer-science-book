"""go_back_n.py: up to W packets in flight, k-bit sequence numbers, cumulative acks."""
from channel import Link, Sim


class Sender:
    def __init__(self, sim, data, k, window, timeout):
        assert window <= 2**k - 1, "go-back-N needs W <= 2^k - 1"
        self.sim, self.data, self.timeout = sim, data, timeout
        self.M, self.W = 2**k, window
        self.base = self.next = 0                # absolute packet numbers
        self.timer, self.link = 0, None

    def fill(self):
        while self.next < len(self.data) and self.next < self.base + self.W:
            self.link.send((self.next % self.M, self.data[self.next]))
            if self.next == self.base:
                self.arm()
            self.next += 1

    def arm(self):
        self.timer += 1
        self.sim.at(self.sim.now + self.timeout, self.expire, self.timer)

    def expire(self, timer):
        if timer == self.timer and self.base < self.next:
            self.next = self.base                # go back: resend the whole window
            self.fill()

    def on_ack(self, seq):
        offset = (seq - self.base) % self.M      # how far past base this ack reaches
        if offset < self.next - self.base:
            self.base += offset + 1              # cumulative: all up to seq arrived
            if self.base < self.next:
                self.arm()
            else:
                self.timer += 1                  # nothing in flight: no timer
            self.fill()


class Receiver:
    def __init__(self, k):
        self.M, self.expected, self.out, self.link = 2**k, 0, [], None
        self.clock, self.done = None, 0.0

    def on_packet(self, packet):
        seq, item = packet
        if seq == self.expected % self.M:        # the next one in order: accept
            self.out.append(item)
            self.expected += 1
            self.done = self.clock.now           # time of the last delivery
        self.link.send((self.expected - 1) % self.M)   # ack the last in-order packet


def transfer(data, k=3, window=7, timeout=150.0, receiver=Receiver, sender=Sender,
             **link):
    sim = Sim()
    s, r = sender(sim, data, k, window, timeout), receiver(k)
    r.clock = sim
    s.link = Link(sim, r.on_packet, **link)
    r.link = Link(sim, s.on_ack, **dict(link, seed=link.get("seed", 0) + 1))
    s.fill()
    sim.run()
    return r.out, r.done, s.link


if __name__ == "__main__":
    data = list(range(5000))
    print("no loss: link utilisation against the window (RTT 100 ms, 1 ms per packet)")
    for w in (1, 7, 31, 127):
        k = (w + 1).bit_length() - 1
        out, t, link = transfer(data, k=k, window=w)
        u, formula = len(data) * 1.0 / t, min(1, w * 1.0 / (100 + 1.0))
        print(f"  W {w:3}: measured {u:.3f}, formula {formula:.3f}")
    print("loss 5 %, duplicates 2 %, W 31:")
    out, t, link = transfer(data, k=5, window=31, loss=0.05, dup=0.02, seed=3)
    print(f"  intact {out == data}, {link.sent} sent for {len(data)}, {t / 1000:.1f} s")
