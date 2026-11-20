"""edit_distance.py: the edit distance of two words, its table, an optimal alignment."""


def table(a, b):
    """d[i][j]: the edit distance of a[:i] and b[:j]."""
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i  # delete the i letters
    for j in range(len(b) + 1):
        d[0][j] = j  # insert the j letters
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1,  # delete a[i-1]
                          d[i][j - 1] + 1,  # insert b[j-1]
                          d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))  # keep or change
    return d


def alignment(a, b, d):
    """Walk back from the corner, following a choice that gives each cell its value."""
    i, j, top, bottom = len(a), len(b), [], []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and d[i][j] == d[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            top.append(a[i - 1])
            bottom.append(b[j - 1])
            i, j = i - 1, j - 1
        elif i > 0 and d[i][j] == d[i - 1][j] + 1:
            top.append(a[i - 1])
            bottom.append("-")
            i -= 1
        else:
            top.append("-")
            bottom.append(b[j - 1])
            j -= 1
    return "".join(reversed(top)), "".join(reversed(bottom))


def main():
    a, b = "train", "rains"
    d = table(a, b)
    print("     " + "  ".join(" " + b))
    for i, row in enumerate(d):
        print(f"  {(' ' + a)[i]} " + " ".join(f"{x:2}" for x in row))
    for a, b in (("train", "rains"), ("catlaogue", "catalogue")):
        d = table(a, b)
        top, bottom = alignment(a, b, d)
        marks = "".join(" " if x == y else "*" for x, y in zip(top, bottom))
        print(f"{a} -> {b}: distance {d[-1][-1]}")
        print("  " + top + "\n  " + bottom + "\n  " + marks.rstrip())


if __name__ == "__main__":
    main()
