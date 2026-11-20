def linear_search(items, target):
    """The position of target in items, or -1; also the number of comparisons."""
    comparisons = 0
    for i in range(len(items)):
        comparisons = comparisons + 1
        if items[i] == target:
            return i, comparisons
    return -1, comparisons


if __name__ == "__main__":
    ages = [12, 9, 15, 11, 9, 14, 13, 10]
    for target in [12, 13, 7]:
        print(target, linear_search(ages, target))
