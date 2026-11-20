"""three_c.py: classify every miss as compulsory, capacity or conflict (exercise 7)."""
from cache import Cache


def classify(addresses, size, line, ways):
    """Runs the trace on the cache and on a fully associative LRU cache as large."""
    cache = Cache(size, line, ways)
    shadow = Cache(size, line, size // line)   # same capacity, no conflict possible
    seen = set()
    counts = {"compulsory": 0, "capacity": 0, "conflict": 0}
    for addr in addresses:
        hit = cache.access(addr)
        shadow_hit = shadow.access(addr)
        block = addr // line
        if not hit:
            if block not in seen:
                counts["compulsory"] += 1      # first use of the line: any cache misses
            elif not shadow_hit:
                counts["capacity"] += 1        # even full associativity misses
            else:
                counts["conflict"] += 1        # only the mapping made it miss
        seen.add(block)
    return cache.misses, counts
