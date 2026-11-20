"""ipv6_compress.py: the canonical text form of an IPv6 address (exercise 12)."""


def compress(groups):
    """Eight 16-bit integers -> the text the standard recommends."""
    best_start, best_len, i = -1, 1, 0         # runs of length 1 are never shortened
    while i < 8:
        if groups[i] == 0:
            j = i
            while j < 8 and groups[j] == 0:
                j += 1
            if j - i > best_len:               # strictly longer: the first one wins
                best_start, best_len = i, j - i
            i = j
        else:
            i += 1
    text = [f"{g:x}" for g in groups]
    if best_start < 0:
        return ":".join(text)
    left = ":".join(text[:best_start])
    right = ":".join(text[best_start + best_len:])
    return left + "::" + right
