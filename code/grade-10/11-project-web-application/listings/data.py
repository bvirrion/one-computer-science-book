"""The library's tables, read once: the books by number, and the loans of each book."""
import csv
from pathlib import Path

HERE = Path(__file__).parent


def read(name):
    with open(HERE / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


BOOKS = {int(b["book_id"]): b for b in read("books.csv")}
LOANS = {}  # book number -> its loans, oldest first
for loan in read("loans.csv"):
    LOANS.setdefault(int(loan["book_id"]), []).append(loan)
MEMBERS = {int(m["member_id"]) for m in read("members.csv")}
