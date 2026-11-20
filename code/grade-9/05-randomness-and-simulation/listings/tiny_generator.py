def next_number(x):
    """A tiny generator: multiply by 5, add 3, keep the remainder by 16."""
    return (5 * x + 3) % 16


x = 7                                    # the starting number
seen = []
while x not in seen:
    seen.append(x)
    x = next_number(x)
print(seen)
print("back to", x, "after", len(seen), "numbers")
