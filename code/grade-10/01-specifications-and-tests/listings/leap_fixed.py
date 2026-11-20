def leap_year(year):
    """Return True if year is a leap year of the Gregorian calendar.

    Precondition: year is a whole number, 1583 or later.
    Postcondition: the result is True exactly when year is divisible
    by 4 and not by 100, or divisible by 400.
    """
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0
