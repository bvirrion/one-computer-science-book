"""boyer_moore.py: Boyer-Moore with the bad-character rule only."""


def last_occurrence(pattern):
    """For each letter of the pattern, its last position; other letters: -1."""
    return {c: j for j, c in enumerate(pattern)}


def boyer_moore(text, pattern):
    """The shifts where pattern occurs, comparing from the right; the comparisons."""
    n, m = len(text), len(pattern)
    last = last_occurrence(pattern)
    found, comparisons, s = [], 0, 0
    while s <= n - m:
        j = m - 1
        while j >= 0:
            comparisons += 1
            if text[s + j] != pattern[j]:
                break
            j -= 1
        if j < 0:
            found.append(s)
            s += 1  # an occurrence: the next shift
        else:  # bring the last c of the pattern under the text's c, or past it
            s += max(1, j - last.get(text[s + j], -1))
    return found, comparisons
