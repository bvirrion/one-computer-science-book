"""exo_mask.py: a mask built one bit short (exercise 2)."""
from cidr import dotted, parse


def mask_wrong(length):
    return (0xFFFFFFFF << (32 - length + 1)) & 0xFFFFFFFF


a, p = parse("203.0.113.77/26")
print("mask   ", dotted(mask_wrong(p)))
print("network", dotted(a & mask_wrong(p)))
b, _ = parse("203.0.113.10")
print("contains 203.0.113.10:", b & mask_wrong(p) == a & mask_wrong(p))
