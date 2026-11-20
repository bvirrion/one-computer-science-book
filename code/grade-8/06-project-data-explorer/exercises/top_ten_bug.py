def most_borrowed_first(row):
    return [-row["loans"], row["title"]]


def top_ten(books, loans):
    counts = {}
    for loan in loans:
        counts[loan["book_id"]] = counts.get(loan["book_id"], 0) + 1
    finder = {}
    for book in books:
        finder[book["book_id"]] = book
    rows = []
    for loan in loans:
        book = finder[loan["book_id"]]
        rows.append({"title": book["title"], "loans": counts[loan["book_id"]]})
    return sorted(rows, key=most_borrowed_first)[:10]
