"""exo_kmp_bug.py: a shorter KMP search, tested against str.find."""
from kmp import failure


def kmp_short(text, pattern):
    pi, q, found = failure(pattern), 0, []
    for i, c in enumerate(text):
        if pattern[q] == c:
            q += 1
        else:
            q = pi[q]
        if q == len(pattern):
            found.append(i - q + 1)
            q = pi[q]
    return found


for text, pattern in [("abcabd", "abd"), ("aaab", "aab"), ("abababc", "ababc"),
                      ("On 2025-12-1, On 2025-12-12", "2025-12-12")]:
    expected = [i for i in range(len(text)) if text.startswith(pattern, i)]
    print(f"{text!r:30} {pattern!r:13} {kmp_short(text, pattern)} expected {expected}")
