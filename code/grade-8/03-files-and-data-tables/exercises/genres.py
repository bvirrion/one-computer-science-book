def count_genres(books):
    """How many books of each genre, in a list of records read with DictReader."""
    counts = {}
    for book in books:
        counts[book["genre"]] = counts.get(book["genre"], 0) + 1
    return counts
