"""spell.py: misspelt queries against the 80 titles of the catalogue: the nearest
title by edit distance, by brute force and with pruning by the triangle inequality."""

import csv
from pathlib import Path

from edit_two_rows import distance

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"
QUERIES = ["the clokwork harbor", "a map of the lighthose", "notes on the libary",
           "the silent comit", "beyond the rivr", "under the gardn", "seven machnie",
           "the hiden kingdom"]


def titles():
    with open(TOWN / "books.csv", newline="") as f:
        return [row["title"].lower() for row in csv.DictReader(f)]


def nearest_brute(query, books):
    return min((distance(query, t), t) for t in books)


def nearest_pruned(query, books, pivots, to_pivot):
    """to_pivot[t][k] = distance(t, pivots[k]), computed once for the catalogue.
    By the triangle inequality, |d(q, p) - d(p, t)| <= d(q, t) for every pivot p."""
    computed = len(pivots)
    dq = [distance(query, p) for p in pivots]
    bound = {t: max(abs(x - y) for x, y in zip(dq, to_pivot[t])) for t in books}
    best = (float("inf"), None)
    for t in sorted(books, key=lambda t: bound[t]):  # most promising first
        if bound[t] >= best[0]:
            break  # every remaining title is at least as far as the best found
        best = min(best, (distance(query, t), t))
        computed += 1
    return best, computed


def main():
    books = titles()
    pivots = books[:4]
    to_pivot = {t: [distance(t, p) for p in pivots] for t in books}
    total = 0
    for q in QUERIES:
        (d, t), computed = nearest_pruned(q, books, pivots, to_pivot)
        assert (d, t) == nearest_brute(q, books)
        total += computed
        print(f"{q!r:26} -> {t!r:26} distance {d}, {computed:2} distances computed")
    print(f"pruned: {total} distances for {len(QUERIES)} queries;"
          f" brute force: {len(QUERIES) * len(books)}")


if __name__ == "__main__":
    main()
