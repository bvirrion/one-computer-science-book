books = [
    {"title": "The Lighthouse Cat", "author": "Mara Quill", "year": 1998},
    {"title": "Seven Bridges", "author": "Tom Alder", "year": 2011},
    {"title": "Rain on Hilltop", "author": "June Okafor", "year": 2004},
]
for book in books:
    print(book["year"], book["title"], "by", book["author"])

recent = 0
for book in books:
    if book["year"] > 2000:
        recent = recent + 1
print(recent, "of", len(books), "books are from after 2000")
