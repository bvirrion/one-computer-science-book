"""contains.py: does a prefix contain an address? (exercise 3)"""
from cidr import mask, parse


def contains(prefix, address):
    net, length = parse(prefix)
    addr, _ = parse(address)
    return addr & mask(length) == net & mask(length)
