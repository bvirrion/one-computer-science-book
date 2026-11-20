books = [
    {"title": "The Lighthouse Cat", "author": "Mara Quill", "year": 1998},
    {"title": "Seven Bridges", "author": "Tom Alder", "year": 2011},
    {"title": "Rain on Hilltop", "author": "June Okafor", "year": 2004},
]


def oldest(books):
    best = books[0]
    for book in books:
        if book["year"] < best["year"]:
            best = book
    return best


print(oldest(books)["title"])
