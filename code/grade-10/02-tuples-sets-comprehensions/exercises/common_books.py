"""Exercise 7: the books two members have both borrowed, with sets."""


def common_books(loans, a, b):
    """Return the set of book ids borrowed both by member a and by member b.

    Precondition: loans is a list of dictionaries with keys "member_id", "book_id".
    """
    books_a = {loan["book_id"] for loan in loans if loan["member_id"] == a}
    books_b = {loan["book_id"] for loan in loans if loan["member_id"] == b}
    return books_a & books_b
