import town

loans = town.load("loans")


def books_of(member):
    """Return the set of the ids of the books that member borrowed."""
    result = set()
    for loan in loans:
        if loan["member_id"] == member:
            result.add(loan["book_id"])
    return result


first = books_of(40)
second = books_of(55)
print("member 40:", sorted(first))
print("member 55:", sorted(second))
print("both:     ", sorted(first & second))
print("sizes:", len(first), len(second), len(first & second), len(first | second))
