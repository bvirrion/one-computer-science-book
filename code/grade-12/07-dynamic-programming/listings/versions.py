"""Two versions of a notice: how far apart are they, word by word?"""
from align import alignment, distance_table
from lcs import lcs_table

OLD = """The library on Town Square opens at nine every morning except Sunday. Children
may borrow four books at a time for three weeks. Late books cost ten cents a day.
The reading room on the first floor closes at six, and the archive is open on
Tuesday and Thursday afternoons by appointment only."""

NEW = """The library on Town Square opens at eight every morning except Sunday and
Monday. Children may borrow six books at a time for three weeks. Late books cost
nothing. The reading room on the second floor closes at seven, and the
archive is open on Tuesday afternoons by appointment."""


def distance_two_rows(a, b):
    """The same distance, keeping only the previous row of the table."""
    previous = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        current = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            change = 0 if a[i - 1] == b[j - 1] else 1
            current[j] = min(previous[j - 1] + change, previous[j] + 1,
                             current[j - 1] + 1)
        previous = current
    return previous[len(b)]


a, b = OLD.split(), NEW.split()
n, m = len(a), len(b)
print("words:", n, "and", m, "| common subsequence:", lcs_table(a, b)[n][m], "words")
d = distance_table(a, b)
print("edit distance:", d[n][m], "| with two rows:", distance_two_rows(a, b))
for x, y in alignment(a, b, d):
    if x != y:
        print(f"  {x or '':>14} -> {y or ''}")
print("cells: full table", (n + 1) * (m + 1), "| two rows", 2 * (m + 1))
