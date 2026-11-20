def percent(part, whole):
    """Return part as a percentage of whole.

    Preconditions: whole > 0 and 0 <= part <= whole.
    Postcondition: the result lies between 0 and 100.
    """
    assert whole > 0, "whole must be positive"
    assert 0 <= part <= whole, "part must lie between 0 and whole"
    result = 100 * part / whole
    assert 0 <= result <= 100
    return result
