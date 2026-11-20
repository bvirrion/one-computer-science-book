"""The network part of an address, by hand: an AND with the mask."""
import ipaddress


def to_int(dotted):
    a, b, c, d = (int(x) for x in dotted.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def to_dotted(n):
    return ".".join(str((n >> shift) & 255) for shift in (24, 16, 8, 0))


def mask(prefix):
    return (2**32 - 1) ^ (2**(32 - prefix) - 1)  # prefix ones, then zeros


address, prefix = "192.0.2.37", 26
print(f"address {to_int(address):032b}")
print(f"mask    {mask(prefix):032b}  = {to_dotted(mask(prefix))}")
network = to_int(address) & mask(prefix)
print(f"AND     {network:032b}  = {to_dotted(network)}")
print("module:", ipaddress.ip_interface(f"{address}/{prefix}").network)
