def busiest_month(loans):
    """The month (01 to 12) in which the most loans went out, and their number."""
    counts = {}
    for loan in loans:
        month = loan["out_date"][5:7]
        counts[month] = counts.get(month, 0) + 1
    best = "01"
    for month in counts:
        if counts[month] > counts.get(best, 0):
            best = month
    return best, counts[best]
