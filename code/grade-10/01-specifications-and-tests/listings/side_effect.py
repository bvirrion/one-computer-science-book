def largest_three(t):
    """Return the three largest numbers of the list t, largest first."""
    t.sort(reverse=True)
    return t[:3]


scores = [12, 18, 7, 15, 9]
print(largest_three(scores))
print(scores)
