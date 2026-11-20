def invert(d):
    """Swap keys and values; the values must all be different."""
    result = {}
    for key, value in d.items():
        result[value] = key
    return result


print(invert({"one": 1, "two": 2, "three": 3}))
