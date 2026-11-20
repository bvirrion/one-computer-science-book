def comes_before(a, b):
    """True when book a goes before book b: older first, then by title."""
    if int(a["year"]) != int(b["year"]):
        return int(a["year"]) < int(b["year"])
    return a["title"] < b["title"]


def sort_books(books):
    """Insertion sort of a list of book records, in place."""
    for i in range(1, len(books)):
        j = i
        while j > 0 and comes_before(books[j], books[j - 1]):
            books[j - 1], books[j] = books[j], books[j - 1]
            j = j - 1
