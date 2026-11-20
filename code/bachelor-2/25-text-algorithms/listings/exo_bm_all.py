"""exo_bm_all.py: after an occurrence, Boyer-Moore shifts by the period m - pi[m]."""
from boyer_moore import boyer_moore, last_occurrence
from kmp import failure
from text_gen import archive


def boyer_moore_all(text, pattern):
    n, m = len(text), len(pattern)
    last, period = last_occurrence(pattern), m - failure(pattern)[m]
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
            s += period  # no occurrence starts closer: it would give a longer border
        else:
            s += max(1, j - last.get(text[s + j], -1))
    return found, comparisons


for text, pattern in [("abababababa", "aba"), ("a" * 30, "aaaaa"),
                      (archive(), "On 2025-12")]:
    (f1, c1), (f2, c2) = boyer_moore(text, pattern), boyer_moore_all(text, pattern)
    assert f1 == f2 == [i for i in range(len(text)) if text.startswith(pattern, i)]
    print(f"{pattern!r:13} {len(f1):3} occurrences; comparisons {c1:5} -> {c2:5}")
