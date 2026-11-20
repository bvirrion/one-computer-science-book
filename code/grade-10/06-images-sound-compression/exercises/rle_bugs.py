"""Exercise 6: a run-length encoder that forgets its last run, and a decoder."""


def rle_encode_buggy(s):
    runs = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            runs.append((count, s[i - 1]))
            count = 1
    return runs


def rle_encode(s):
    runs = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            runs.append((count, s[i - 1]))
            count = 1
    if s:
        runs.append((count, s[-1]))
    return runs
