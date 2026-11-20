def nested_sum(item):
    """The sum of all numbers in item: a number, or a list of items."""
    if not isinstance(item, list):
        return item
    return sum(nested_sum(x) for x in item)


marks = [12, [15, 9], [[8, 11], 14], [], [[[20]]]]
print(nested_sum(marks))
print(nested_sum(7), nested_sum([]))
