import csv

with open("books.csv", encoding="utf-8") as f:
    books = list(csv.DictReader(f))

print(len(books), "books")
print(books[0])
print(books[0]["pages"], type(books[0]["pages"]))
pages = int(books[0]["pages"])
print(pages + 1, type(pages))
