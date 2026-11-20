def factorial(n, depth=0):
    print("    " * depth + f"factorial({n}) called")
    if n == 0:
        result = 1
    else:
        result = n * factorial(n - 1, depth + 1)
    print("    " * depth + f"factorial({n}) returns {result}")
    return result


factorial(4)
