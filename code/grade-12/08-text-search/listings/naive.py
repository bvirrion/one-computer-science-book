"""The naive search: try the pattern at every position of the text."""


def search_naive(text, p):
    """Return the positions where p occurs in text, and the comparisons made."""
    n, m = len(text), len(p)
    positions, comparisons = [], 0
    for i in range(n - m + 1):              # every alignment of p under text
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != p[j]:
                break                       # mismatch: give up this alignment
            j += 1
        if j == m:
            positions.append(i)
    return positions, comparisons


if __name__ == "__main__":
    text = "a man a plan a canal panama"
    print(search_naive(text, "an"))
    print(search_naive(text, "canal"))
    print(search_naive(text, "pan"), search_naive(text, "boat"))
