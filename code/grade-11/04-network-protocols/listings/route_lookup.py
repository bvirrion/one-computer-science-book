"""A router's table, read by longest prefix match."""
import ipaddress

TABLE = [  # destination, next hop
    ("192.0.2.0/24", "direct, port 1"),
    ("198.51.100.0/24", "router B"),
    ("198.51.100.128/25", "router C"),
    ("0.0.0.0/0", "router D (default)"),
]


def lookup(address):
    address = ipaddress.ip_address(address)
    best = None
    for dest, hop in TABLE:
        net = ipaddress.ip_network(dest)
        if address in net and (best is None or net.prefixlen > best[0].prefixlen):
            best = (net, hop)
    return best


for a in ["192.0.2.99", "198.51.100.7", "198.51.100.200", "203.0.113.5"]:
    net, hop = lookup(a)
    print(f"{a:16} matches {str(net):19} -> {hop}")
