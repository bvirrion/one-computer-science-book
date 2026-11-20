# capture: exit
def average(t):
    """Return the mean of the numbers in the list t.

    Precondition: t is a non-empty list of numbers.
    """
    assert len(t) > 0, "average of an empty list"
    total = 0
    for x in t:
        total = total + x
    return total / len(t)


print(average([12, 15, 9]))
print(average([]))
