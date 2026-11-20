def most_loans(loans):
    """The member_id with the most loans, and its number of loans."""
    counts = {}
    for loan in loans:
        counts[loan["member_id"]] = counts.get(loan["member_id"], 0) + 1
    best = ""
    for member in counts:
        if best == "" or counts[member] > counts[best]:
            best = member
    return best, counts[best]
