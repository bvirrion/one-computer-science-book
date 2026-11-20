def min_max(t):
    """Return the smallest and the largest number of the non-empty list t."""
    smallest = t[0]
    largest = t[0]
    for x in t:
        if x < smallest:
            smallest = x
        if x > largest:
            largest = x
    return smallest, largest


low, high = min_max([12, 18, 7, 15, 9])
print("lowest", low, "highest", high)
print(min_max([5]))
