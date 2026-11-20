from datetime import date


def average_length(loans):
    """The average number of days between going out and coming back."""
    days = 0
    returned = 0
    for loan in loans:
        if loan["return_date"] != "":
            start = date.fromisoformat(loan["out_date"])
            end = date.fromisoformat(loan["return_date"])
            days = days + (end - start).days
            returned = returned + 1
    return round(days / returned, 1)
