def total_pages(books):
    total = 0
    for book in books:
        total = total + int(book["pages"])
    return total
