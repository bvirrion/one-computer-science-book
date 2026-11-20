"""flush.py: how many memory writes a write-back cache still owes (exercise 3)."""


def dirty_lines(cache):
    """The lines that must be written to memory if the cache is emptied now."""
    return sum(dirty for s in cache.data for dirty in s.values())


def total_writes(cache):
    """Writes to memory so far, plus those that emptying the cache would add."""
    return cache.memory_writes + dirty_lines(cache)
