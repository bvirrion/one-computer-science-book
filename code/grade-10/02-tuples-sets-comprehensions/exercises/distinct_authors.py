"""Exercise 11: the authors of the town library, without repeats."""


def distinct_authors(books):
    """Return the set of the authors of the list of book records books."""
    return {book["author"] for book in books}


def authors_in_genre(books, genre):
    """Return the sorted list of the authors of at least one book of the genre."""
    return sorted({book["author"] for book in books if book["genre"] == genre})
