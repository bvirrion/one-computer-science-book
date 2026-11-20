"""lpm_trie.py: longest-prefix match on a binary trie of the forwarding table."""
from cidr import parse


class Trie:
    def __init__(self):
        self.root = {}                 # a node: {0: child, 1: child, "hop": port}

    def insert(self, prefix, hop):
        addr, length = parse(prefix)
        node = self.root
        for i in range(length):                # one level per bit of the prefix
            node = node.setdefault(addr >> (31 - i) & 1, {})
        node["hop"] = hop

    def lookup(self, address):
        """The hop of the longest prefix containing address, and the steps taken."""
        addr, _ = parse(address)
        node, best, steps = self.root, self.root.get("hop"), 0
        while steps < 32 and (addr >> (31 - steps) & 1) in node:
            node = node[addr >> (31 - steps) & 1]
            steps += 1
            best = node.get("hop", best)       # a longer prefix overrides
        return best, steps


if __name__ == "__main__":
    table = [("0.0.0.0/0", "port 0 (default)"), ("198.51.100.0/24", "port 1"),
             ("198.51.100.128/25", "port 2"), ("203.0.113.0/24", "port 3"),
             ("203.0.113.64/26", "port 4")]
    t = Trie()
    for prefix, hop in table:
        t.insert(prefix, hop)
    for a in ["198.51.100.7", "198.51.100.200", "203.0.113.77", "203.0.113.5",
              "192.0.2.1"]:
        hop, steps = t.lookup(a)
        print(f"{a:15} -> {hop:17} ({steps} steps)")
