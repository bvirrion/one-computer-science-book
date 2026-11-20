"""Exercises of the chapter on searching in text."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from horspool import horspool  # noqa: E402
from shift_table import shift_table  # noqa: E402


def count_occurrences(text, p):                    # exercise 5
    count = 0
    for i in range(len(text) - len(p) + 1):
        if text[i:i + len(p)] == p:
            count += 1
    return count


def search_naive_short(text, p):                   # exercise 6: the staged fault
    return [i for i in range(len(text) - len(p)) if text[i:i + len(p)] == p]


def horspool_first(text, p):                       # exercise 7
    n, m = len(text), len(p)
    shift, i = shift_table(p), 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == p[j]:
            j -= 1
        if j < 0:
            return i                               # stop at the first occurrence
        i += shift.get(text[i + m - 1], m)
    return -1


def shift_table_bad(p):                            # exercise 8: the staged fault
    return {p[j]: len(p) - 1 - j for j in range(len(p))}   # the last letter too


def search_ignore_case(text, p):                   # exercise 11
    return horspool(text.lower(), p.lower())[0]


def search_wildcard(text, p):                      # exercise 14: '?' matches any letter
    n, m = len(text), len(p)
    found = []
    for i in range(n - m + 1):
        if all(p[j] == "?" or p[j] == text[i + j] for j in range(m)):
            found.append(i)
    return found


def mean_jump_measured(n, m, seed):                # exercise 15
    import random
    rng = random.Random(seed)
    text = "".join(rng.choice("ACGT") for _ in range(n))
    start = rng.randrange(n - m)
    table = shift_table(text[start:start + m])
    i, jumps = 0, []
    while i <= n - m:
        jumps.append(table.get(text[i + m - 1], m))
        i += jumps[-1]
    table_mean = sum(table.get(c, m) for c in "ACGT") / 4
    return table, table_mean, len(jumps), sum(jumps) / len(jumps)


if __name__ == "__main__":
    print(count_occurrences("ABABABAB", "ABAB"), search_naive_short("the town", "town"))
    print(horspool_first("the bus to the station", "station"), shift_table_bad("TOWN"))
    print(search_ignore_case("The Town and the town", "TOWN"))
    print(search_wildcard("the bus to the station stops", "st?"))
