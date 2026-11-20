"""source.py -- the text source of this chapter: the titles of the books in Brenmoor's
library catalogue, lower case, letters and spaces only, one space between titles."""
import csv
from pathlib import Path

BOOKS = Path(__file__).resolve().parents[4] / "data" / "town" / "books.csv"


def catalogue_text():
    titles = [r["title"].lower() for r in csv.DictReader(open(BOOKS))]
    text = " ".join(titles)
    return "".join(ch for ch in text if ch.isalpha() or ch == " ")
