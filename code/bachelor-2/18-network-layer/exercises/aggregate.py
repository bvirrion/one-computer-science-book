"""aggregate.py: the fewest prefixes that cover the same addresses."""
from cidr import dotted, mask, parse


def aggregate(prefixes):
    """Prefixes with the same next hop, as text; returns a minimal equivalent list."""
    nets = {(n & mask(p), p) for n, p in map(parse, prefixes)}
    changed = True
    while changed:
        changed = False
        for n, p in sorted(nets, key=lambda x: -x[1]):
            if (n, p) not in nets:
                continue
            if any(q < p and n & mask(q) == m for m, q in nets):
                nets.discard((n, p))           # inside a shorter prefix: redundant
                changed = True
                continue
            sibling = n ^ (1 << (32 - p)) if p > 0 else None
            if sibling is not None and (sibling, p) in nets:
                nets -= {(n, p), (sibling, p)}
                nets.add((n & mask(p - 1), p - 1))   # two halves make the whole
                changed = True
    return [f"{dotted(n)}/{p}" for n, p in sorted(nets)]
