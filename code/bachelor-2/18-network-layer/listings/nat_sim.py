"""nat_sim.py: a home router maps private addresses and ports to its own."""
PUBLIC = "203.0.113.7"


class NAT:
    def __init__(self):
        self.out, self.back, self.next_port = {}, {}, 40000

    def outbound(self, src, sport, dst, dport):
        key = (src, sport)
        if key not in self.out:                # a new conversation: a new public port
            self.out[key], self.back[self.next_port] = self.next_port, key
            self.next_port += 1
        return PUBLIC, self.out[key], dst, dport

    def inbound(self, src, sport, dport):
        if dport not in self.back:
            return None                        # nobody inside asked: dropped
        inside, iport = self.back[dport]
        return src, sport, inside, iport


if __name__ == "__main__":
    nat = NAT()
    for src, sport in [("192.168.1.10", 50000), ("192.168.1.11", 50000),
                       ("192.168.1.10", 50001)]:
        s, p, d, dp = nat.outbound(src, sport, "198.51.100.20", 80)
        print(f"out {src}:{sport} -> {d}:{dp}   becomes {s}:{p} -> {d}:{dp}")
    for dport in (40001, 40007):
        r = nat.inbound("198.51.100.20", 80, dport)
        to = f"delivered to {r[2]}:{r[3]}" if r else "dropped: no entry"
        print(f"in  198.51.100.20:80 -> {PUBLIC}:{dport}   {to}")
