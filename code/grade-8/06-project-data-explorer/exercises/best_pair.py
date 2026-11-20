def best_pair(loans):
    """The pair of books borrowed by the most members, and that number of members."""
    books_of = {}
    for loan in loans:
        member = loan["member_id"]
        if member not in books_of:
            books_of[member] = []
        if loan["book_id"] not in books_of[member]:
            books_of[member].append(loan["book_id"])
    pairs = {}
    for member in books_of:
        ids = sorted(books_of[member], key=int)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                pair = ids[i] + "+" + ids[j]
                pairs[pair] = pairs.get(pair, 0) + 1
    best = ""
    for pair in pairs:
        if best == "" or pairs[pair] > pairs[best]:
            best = pair
    return best, pairs[best]
