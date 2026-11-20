def worst_guesses(n):
    """Guesses of binary search on n items, the target always in the larger half."""
    low = 0
    high = n - 1
    guesses = 0
    while low <= high:
        middle = (low + high) // 2
        guesses = guesses + 1
        low = middle + 1            # the right half is never smaller than the left
    return guesses


n = 10
while n <= 1_000_000:
    print(f"{n:>9} items: {worst_guesses(n)} guesses at most")
    n = n * 10
