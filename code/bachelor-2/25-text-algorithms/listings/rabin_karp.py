"""rabin_karp.py: a rolling hash modulo q; a window whose hash equals the pattern's is
checked letter by letter, and a failed check is a spurious hit."""

BASE = 256


def rabin_karp(text, pattern, q):
    """The occurrences, and the number of spurious hits."""
    n, m = len(text), len(pattern)
    if m > n:
        return [], 0
    high = pow(BASE, m - 1, q)  # the weight of the window's first letter
    hp = hw = 0
    for j in range(m):
        hp = (hp * BASE + ord(pattern[j])) % q
        hw = (hw * BASE + ord(text[j])) % q
    found, spurious = [], 0
    for s in range(n - m + 1):
        if hw == hp:
            if text[s:s + m] == pattern:
                found.append(s)
            else:
                spurious += 1
        if s < n - m:  # roll: remove text[s], append text[s + m]
            hw = ((hw - ord(text[s]) * high) * BASE + ord(text[s + m])) % q
    return found, spurious
