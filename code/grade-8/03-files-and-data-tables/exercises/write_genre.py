import csv


def write_genre(books, genre, filename):
    """Write the books of one genre to a new CSV file, with the same header row."""
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(books[0].keys()))
        writer.writeheader()
        for book in books:
            if book["genre"] == genre:
                writer.writerow(book)
