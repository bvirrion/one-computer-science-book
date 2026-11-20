"""kmp.py: Knuth-Morris-Pratt: the failure function, then a search that never moves back
in the text."""


def failure(pattern):
    """pi[q] = the length of the longest proper border of pattern[:q], for q = 1..m."""
    m = len(pattern)
    pi = [0] * (m + 1)
    k = 0  # the length of the current border
    for q in range(2, m + 1):
        while k > 0 and pattern[k] != pattern[q - 1]:
            k = pi[k]  # the next shorter border
        if pattern[k] == pattern[q - 1]:
            k += 1
        pi[q] = k
    return pi


def kmp(text, pattern):
    """The shifts where pattern occurs in text, and the letter comparisons made."""
    pi, n, m = failure(pattern), len(text), len(pattern)
    found, comparisons, q = [], 0, 0  # q letters of the pattern are matched
    for i, c in enumerate(text):
        while True:
            if i - q > n - m:  # the pattern now starts too far right to fit
                return found, comparisons
            comparisons += 1
            if pattern[q] == c:
                q += 1
                break
            if q == 0:
                break
            q = pi[q]  # shift the pattern; compare c again
        if q == m:
            found.append(i - m + 1)
            q = pi[q]
    return found, comparisons


if __name__ == "__main__":
    for pattern in ["ababc", "abcabd", "aaaab", "On 2025-0"]:
        pi = failure(pattern)
        pairs = " ".join(f"{q}:{pi[q]}" for q in range(1, len(pattern) + 1))
        print(f"{pattern!r:12}", pairs)
