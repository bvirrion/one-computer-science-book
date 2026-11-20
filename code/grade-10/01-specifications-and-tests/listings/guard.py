# capture: exit
def starts_with(t, x):
    """Return True if the list t is not empty and its first element is x."""
    return len(t) > 0 and t[0] == x


def starts_with_unguarded(t, x):
    return t[0] == x


print(starts_with([3, 1, 4], 3))
print(starts_with([], 3))
print(starts_with_unguarded([], 3))
