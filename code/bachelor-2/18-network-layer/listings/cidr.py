"""cidr.py: addresses and prefixes as 32-bit integers, checked against ipaddress."""
import ipaddress


def parse(text):
    """'203.0.113.77/26' -> (address as an integer, prefix length)."""
    addr, _, length = text.partition("/")
    a, b, c, d = (int(x) for x in addr.split("."))
    return a << 24 | b << 16 | c << 8 | d, int(length or 32)


def dotted(n):
    return ".".join(str(n >> s & 0xFF) for s in (24, 16, 8, 0))


def mask(length):
    return (0xFFFFFFFF << (32 - length)) & 0xFFFFFFFF     # length ones, then zeros


def network(addr, length):
    return addr & mask(length)


def broadcast(addr, length):
    return network(addr, length) | (~mask(length) & 0xFFFFFFFF)


if __name__ == "__main__":
    for text in ["203.0.113.77/26", "198.51.100.200/28", "192.0.2.5/30"]:
        a, p = parse(text)
        net, last = network(a, p), broadcast(a, p)
        hosts = max(2 ** (32 - p) - 2, 0)
        print(f"{text:18} mask {dotted(mask(p)):15} network {dotted(net):14} "
              f"broadcast {dotted(last):14} hosts {hosts}")
        ref = ipaddress.ip_interface(text).network
        assert (dotted(net), dotted(last)) == (str(ref.network_address),
                                               str(ref.broadcast_address))
    print(f"{parse('203.0.113.77')[0]:032b}")
