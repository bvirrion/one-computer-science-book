"""The library kept as one wide table: every loan with its book, member and street."""
import town

books = {r["book_id"]: r for r in town.load("books")}
members = {r["member_id"]: r for r in town.load("members")}
people = {r["person_id"]: r for r in town.load("people")}
streets = {r["street_id"]: r for r in town.load("streets")}

flat = []
for loan in town.load("loans"):                 # one wide row per loan
    member = members[loan["member_id"]]
    person = people[member["person_id"]]
    flat.append({"loan_id": loan["loan_id"], "out_date": loan["out_date"],
                 "title": books[loan["book_id"]]["title"],
                 "author": books[loan["book_id"]]["author"],
                 "member": person["first_name"] + " " + person["last_name"],
                 "street": streets[person["street_id"]]["name"],
                 "postcode": streets[person["street_id"]]["postcode"]})

print(len(flat), "rows of", len(flat[0]), "columns:", ", ".join(flat[0]))
name = flat[1]["member"]
rows = [r for r in flat if r["member"] == name]
print(f"update: if {name} moves, {len(rows)} rows must change")
title = flat[1]["title"]
copies = sum(r["title"] == title for r in flat)
print(f"redundancy: the author of {title!r} is written {copies} times")
print(f"deletion: removing the {copies} old loans of {title!r}",
      "also removes the book and its author")
print("insertion: a new member with no loan has no row to go in;",
      "a new book neither")
