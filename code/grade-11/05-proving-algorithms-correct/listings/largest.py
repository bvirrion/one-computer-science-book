def largest(t):
    """Pre: t is a non-empty list of numbers. Post: returns the largest element of t."""
    best = t[0]
    i = 1
    while i < len(t):
        assert best == max(t[:i])           # invariant: best is the largest of t[:i]
        if t[i] > best:
            best = t[i]
        i = i + 1
    assert i == len(t) and best == max(t)   # at the end: i == len(t), so t[:i] is t
    return best


print(largest([31, 7, 58, 12, 58, 3]))
print(largest([-4]))
