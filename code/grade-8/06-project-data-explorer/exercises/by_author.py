def books_by(books, author):
    """The titles of the books written by author."""
    titles = []
    for book in books:
        if book["author"] == author:
            titles.append(book["title"])
    return titles
