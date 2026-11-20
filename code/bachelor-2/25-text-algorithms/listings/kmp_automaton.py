"""kmp_automaton.py: the string-matching automaton of a pattern, from its failure
function; state q = the number of pattern letters matched."""
from kmp import failure


def automaton(pattern, alphabet):
    """delta[q][c] for q = 0..m: the longest prefix of pattern that is a suffix of
    pattern[:q] + c."""
    pi, m = failure(pattern), len(pattern)
    delta = [{} for _ in range(m + 1)]
    for q in range(m + 1):
        for c in alphabet:
            if q < m and pattern[q] == c:
                delta[q][c] = q + 1
            else:  # the same move as from the longest border (state 0: stay)
                delta[q][c] = delta[pi[q]][c] if q > 0 else 0
    return delta


def run(delta, m, text):
    """One table lookup per letter: the end positions of the occurrences."""
    q, ends = 0, []
    for i, c in enumerate(text):
        q = delta[q].get(c, 0)
        if q == m:
            ends.append(i)
    return ends


if __name__ == "__main__":
    pattern, alphabet = "ababc", "abc"
    delta = automaton(pattern, alphabet)
    print("state  " + "  ".join(alphabet))
    for q, row in enumerate(delta):
        print(f"{q:5}  " + "  ".join(str(row[c]) for c in alphabet))
    text = "abababcababcabc"
    print(f"in {text}: occurrences end at {run(delta, len(pattern), text)}")
