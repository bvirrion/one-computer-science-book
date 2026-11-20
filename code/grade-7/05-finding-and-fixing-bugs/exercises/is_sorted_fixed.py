def is_sorted(values):
    """True when every item is at least as large as the one before it."""
    for i in range(len(values) - 1):
        if not values[i] <= values[i + 1]:
            return False
    return True


print(is_sorted([1, 2, 3]), is_sorted([3, 1]))
print(is_sorted([2, 5, 5, 8]), is_sorted([1, 1]))
