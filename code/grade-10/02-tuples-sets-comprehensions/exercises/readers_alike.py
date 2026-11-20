"""Problem: the two members of the town library whose borrowed books are most alike."""
from fractions import Fraction

import town

loans = town.load("loans")
members = {m["member_id"]: m["person_id"] for m in town.load("members")}
people = {p["person_id"]: f"{p['first_name']} {p['last_name']}"
          for p in town.load("people")}

books = {}
for loan in loans:
    books.setdefault(loan["member_id"], set()).add(loan["book_id"])


def jaccard(a, b):
    return Fraction(len(a & b), len(a | b))


def best_pairs(min_books):
    ids = sorted(m for m in books if len(books[m]) >= min_books)
    pairs = [(jaccard(books[i], books[j]), i, j) for i in ids for j in ids if i < j]
    pairs.sort(key=lambda p: (-p[0], p[1], p[2]))
    return ids, pairs


if __name__ == "__main__":
    print("members who borrowed:", len(books))
    borrowed = set().union(*books.values())
    print("loans:", len(loans), " distinct books borrowed:", len(borrowed))
    for min_books in (1, 5):
        ids, pairs = best_pairs(min_books)
        print(f"at least {min_books} books: {len(ids)} members, {len(pairs)} pairs")
        for value, i, j in pairs[:3]:
            shared = len(books[i] & books[j])
            print(f"  {value} = {float(value):.3f}  members {i} and {j}"
                  f"  ({len(books[i])} and {len(books[j])} books, {shared} shared)")
    value, i, j = best_pairs(5)[1][0]
    print("closest readers:", people[members[i]], "and", people[members[j]])
