from collections import namedtuple

Book = namedtuple("Book", ["title", "author", "year"])

b = Book("The Silent Code", "Fatou Dalewell", 2002)
print(b)
print(b.title, "was published in", b.year)
print(b[2] == b.year)
title, author, year = b
print(author)
