def longest_streak(points):
    """The longest run of right first answers (1 point each) in a list of points."""
    best = 0
    run = 0
    for p in points:
        if p == 1:
            run = run + 1
            if run > best:
                best = run
        else:
            run = 0
    return best


print(longest_streak([1, 0.5, 1, 1, 1, 0, 1, 1, 0.5, 1]))
