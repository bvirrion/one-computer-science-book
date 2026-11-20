"""The longest common subsequence of two words, with its table."""


def lcs_table(a, b):
    n, m = len(a), len(b)
    t = [[0] * (m + 1) for _ in range(n + 1)]   # t[i][j]: for a[:i] and b[:j]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                t[i][j] = t[i - 1][j - 1] + 1
            else:
                t[i][j] = max(t[i - 1][j], t[i][j - 1])
    return t


def rebuild(a, b, t):
    i, j, out = len(a), len(b), []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i, j = i - 1, j - 1
        elif t[i - 1][j] >= t[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


if __name__ == "__main__":
    a, b = "LIBRARY", "LITERARY"
    t = lcs_table(a, b)
    print("    " + " ".join(b))
    for i, row in enumerate(t):
        print((" " + a)[i], " ".join(str(x) for x in row))
    print("length", t[len(a)][len(b)], "subsequence", rebuild(a, b, t))
