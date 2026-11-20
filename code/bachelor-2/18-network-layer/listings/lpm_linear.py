"""lpm_linear.py: longest-prefix match by trying every entry of the table."""
from cidr import network, parse


def lookup(table, address):
    addr, _ = parse(address)
    best, best_len = None, -1
    for prefix, hop in table:
        net, length = parse(prefix)
        if network(addr, length) == net and length > best_len:
            best, best_len = hop, length
    return best
