def late_returns(loans):
    """Loans returned after their due date; dates are compared as YYYY-MM-DD text."""
    late = 0
    for loan in loans:
        if loan["return_date"] != "" and loan["return_date"] > loan["due_date"]:
            late = late + 1
    return late
