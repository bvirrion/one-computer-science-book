"""Searching the titles of the town library, joined into one text."""
import csv

from horspool import horspool
from naive import search_naive

with open("books.csv", newline="") as f:
    titles = [row["title"] for row in csv.DictReader(f)]
text = "\n".join(titles)                    # one title per line
print(len(titles), "titles,", len(text), "letters")
for word in ["Forest", "River", "The", "Lighthouse", "Silent Code"]:
    found, naive_c = search_naive(text, word)
    found_h, hors_c = horspool(text, word)
    lines = [text.count("\n", 0, i) + 1 for i in found_h]
    shown = lines if len(lines) <= 8 else lines[:3] + ["..."]
    print(f"{word!r:14} {len(lines):2} found  naive {naive_c:5}  Horspool {hors_c:4}"
          f"  lines {shown}")
