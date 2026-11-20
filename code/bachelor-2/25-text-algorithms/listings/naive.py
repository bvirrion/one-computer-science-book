"""naive.py: every shift tried, letters compared from the left."""


def naive(text, pattern):
    """The shifts where pattern occurs in text, and the letter comparisons made."""
    n, m = len(text), len(pattern)
    found, comparisons = [], 0
    for s in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[s + j] != pattern[j]:
                break
            j += 1
        if j == m:
            found.append(s)
    return found, comparisons
