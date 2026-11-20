"""Exercise: for each author of at least two books, the members who borrowed every
one of them -- a relational division per author."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from algebra import division, project, select, table  # noqa: E402


def every_book_of(author):
    books, loans = table("books"), table("loans")
    theirs = project(select(books, lambda t: t["author"] == author), ("book_id",))
    return theirs, division(project(loans, ("member_id", "book_id")), theirs)


if __name__ == "__main__":
    authors = {t[0] for t in project(table("books"), ("author",)).rows}
    for author in sorted(authors):
        theirs, readers = every_book_of(author)
        if len(theirs) >= 2 and len(readers):
            print(author, len(theirs), sorted(t[0] for t in readers.rows))
