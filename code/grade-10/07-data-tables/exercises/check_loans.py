"""Exercise 14: consistency checks over the loans table."""
from datetime import date, timedelta


def problems(loans):
    """Return a list of (loan_id, message) for each broken rule."""
    found = []
    for loan in loans:
        out = date.fromisoformat(loan["out_date"])
        if date.fromisoformat(loan["due_date"]) != out + timedelta(days=21):
            found.append((loan["loan_id"], "due date is not 21 days after"))
        back = loan["return_date"]
        if back is not None and date.fromisoformat(back) < out:
            found.append((loan["loan_id"], "returned before it went out"))
    return found
