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
            print("question", choice, "is not ready yet")
        elif choice != "0":
            print("please type a number from 0 to 4")
    print("goodbye")


if __name__ == "__main__":
    main()
