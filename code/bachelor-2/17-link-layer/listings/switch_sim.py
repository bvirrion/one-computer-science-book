"""switch_sim.py: a self-learning switch: learn sources, forward, flood, filter."""


class Switch:
    def __init__(self, ports):
        self.ports = ports
        self.table = {}                       # MAC address -> port

    def receive(self, src, dst, port):
        """Return the ports the frame leaves by."""
        self.table[src] = port                # learn: src is reachable through port
        if dst in self.table:
            out = self.table[dst]
            return [] if out == port else [out]    # filter, or forward
        return [p for p in self.ports if p != port]   # unknown: flood


if __name__ == "__main__":
    hosts = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    sw = Switch(ports=[1, 2, 3, 4, 5])
    for src, dst in ["AB", "BA", "CA", "AC", "EB", "DF"]:
        out = sw.receive(src, dst, hosts[src])
        how = "flood" if len(out) > 1 else "forward"
        table = " ".join(f"{m}:{p}" for m, p in sorted(sw.table.items()))
        print(f"{src} -> {dst}  {how} to {out}  table {table}")
