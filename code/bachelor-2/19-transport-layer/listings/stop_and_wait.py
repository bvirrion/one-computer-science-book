"""stop_and_wait.py: one packet at a time, a 1-bit sequence number, a timer."""
from channel import Link, Sim


class Sender:
    def __init__(self, sim, data, timeout):
        self.sim, self.data, self.timeout = sim, data, timeout
        self.next, self.bit, self.timer = 0, 0, 0
        self.link = None

    def start(self):
        if self.next < len(self.data):
            self.link.send((self.bit, self.data[self.next]))
            self.timer += 1                      # a new timer; older ones are void
            self.sim.at(self.sim.now + self.timeout, self.expire, self.timer)

    def expire(self, timer):
        if timer == self.timer:                  # no acknowledgement came: send again
            self.start()

    def on_ack(self, bit):
        if bit == self.bit:                      # the ack of the packet in flight
            self.next, self.bit = self.next + 1, 1 - self.bit
            self.start()                         # (a duplicate ack is ignored)


class Receiver:
    def __init__(self):
        self.expected, self.out, self.link = 0, [], None
        self.clock, self.done = None, 0.0

    def on_packet(self, packet):
        bit, item = packet
        if bit == self.expected:                 # new data: keep it
            self.out.append(item)
            self.expected = 1 - self.expected
            self.done = self.clock.now
        self.link.send(bit)                      # acknowledge, even a duplicate


def transfer(data, timeout=150.0, **link):
    sim = Sim()
    s, r = Sender(sim, data, timeout), Receiver()
    r.clock = sim
    s.link = Link(sim, r.on_packet, **link)
    r.link = Link(sim, s.on_ack, **dict(link, seed=link.get("seed", 0) + 1))
    s.start()
    sim.run()
    return r.out, r.done, s.link


if __name__ == "__main__":
    data = list(range(200))
    for loss in (0.0, 0.1, 0.3):
        out, t, link = transfer(data, loss=loss, dup=0.05, seed=19)
        print(f"loss {loss:.1f}: delivered intact {out == data}, {link.sent} packets"
              f" sent for {len(data)}, {t / 1000:.1f} s")
