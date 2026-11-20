import csv

MENU = """1. loans by genre
2. the ten most borrowed books
3. books never borrowed
4. loans still out on a date
0. quit"""


def load_table(filename):
    """The records of a CSV file, as a list of dictionaries."""
    with open(filename, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def count_lines(filename):
    """The number of records: the lines of the file, minus the header row."""
    with open(filename, encoding="utf-8") as f:
        return len(f.readlines()) - 1


def book_finder(books):
    """A dictionary that gives the record of a book from its book_id."""
    finder = {}
    for book in books:
        finder[book["book_id"]] = book
    return finder


def loans_by_genre(books, loans):
    """The number of loans of each genre: each loan looks up its book."""
    finder = book_finder(books)
    counts = {}
    for loan in loans:
        genre = finder[loan["book_id"]]["genre"]
        counts[genre] = counts.get(genre, 0) + 1
    return counts


def never_borrowed(books, loans):
    """The titles of the books that no loan mentions."""
    borrowed = {}
    for loan in loans:
        borrowed[loan["book_id"]] = True
    titles = []
    for book in books:
        if book["book_id"] not in borrowed:
            titles.append(book["title"])
    return titles


def most_borrowed_first(row):
    """The sort key: the most loans first, then the title in alphabetical order."""
    return [-row["loans"], row["title"]]


def top_ten(books, loans):
    """The ten most borrowed books, as records with a title and a number of loans."""
    counts = {}
    for loan in loans:
        counts[loan["book_id"]] = counts.get(loan["book_id"], 0) + 1
    rows = []
    for book in books:
        rows.append({"title": book["title"], "loans": counts.get(book["book_id"], 0)})
    return sorted(rows, key=most_borrowed_first)[:10]


def answer(choice, books, loans):
    """The lines of the answer to one question."""
    lines = []
    if choice == "1":
        counts = loans_by_genre(books, loans)
        for genre in sorted(counts):
            lines.append(f"{genre:<10} {counts[genre]:>4}")
    elif choice == "2":
        rank = 1
        for row in top_ten(books, loans):
            lines.append(f"{rank:>2}. {row['title']:<28} {row['loans']:>3}")
            rank = rank + 1
    elif choice == "3":
        titles = never_borrowed(books, loans)
        for title in titles:
            lines.append(title)
        if titles == []:
            lines.append("every book was borrowed at least once")
    else:
        lines.append("question " + choice + " is not ready yet")
    return lines


def main():
    books = load_table("books.csv")
    loans = load_table("loans.csv")
    assert len(books) == count_lines("books.csv")
    assert len(loans) == count_lines("loans.csv")
    print("loaded", len(books), "books and", len(loans), "loans")
    print(MENU)
    choice = ""
    while choice != "0":
        choice = input("choice: ").strip()
        if choice in ["1", "2", "3", "4"]:
            for line in answer(choice, books, loans):
                print(line)
        elif choice != "0":
            print("please type a number from 0 to 4")
    print("goodbye")


if __name__ == "__main__":
    main()
