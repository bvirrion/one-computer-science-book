"""palindrome.py: the longest palindromic subsequence, by an interval table."""


def longest_palindrome(s):
    n = len(s)
    if n == 0:
        return 0
    best = [[0] * n for _ in range(n)]  # best[i][j]: for s[i..j]
    for i in range(n - 1, -1, -1):
        best[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                best[i][j] = best[i + 1][j - 1] + 2 if j > i + 1 else 2
            else:
                best[i][j] = max(best[i + 1][j], best[i][j - 1])
    return best[0][n - 1]
