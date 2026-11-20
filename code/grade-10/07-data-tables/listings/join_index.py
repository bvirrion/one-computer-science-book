from load_weather import read_table

loans = read_table("loans.csv")
books = read_table("books.csv")
members = read_table("members.csv")
people = read_table("people.csv")

book_by_id = {book["book_id"]: book for book in books}  # one pass over books
person_by_id = {p["person_id"]: p for p in people}
member_by_id = {m["member_id"]: m for m in members}

for loan in loans:
    if loan["return_date"] is None and loan["due_date"] < "2025-07-01":
        book = book_by_id[loan["book_id"]]  # one lookup per loan
        person = person_by_id[member_by_id[loan["member_id"]]["person_id"]]
        print(loan["due_date"], book["title"], "-",
              person["first_name"], person["last_name"])
