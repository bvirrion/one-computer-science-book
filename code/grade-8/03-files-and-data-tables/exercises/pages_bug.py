def total_pages(books):
    total = 0
    for book in books:
        total = total + book["pages"]
    return total
