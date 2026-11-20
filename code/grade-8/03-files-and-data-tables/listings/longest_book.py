import csv

with open("books.csv", encoding="utf-8") as f:
    books = list(csv.DictReader(f))

longest = books[0]
for book in books:
    if int(book["pages"]) > int(longest["pages"]):
        longest = book
print(longest["title"], "by", longest["author"], "-", longest["pages"], "pages")
