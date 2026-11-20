def binary_search(items, target):
    """The position of target in the sorted list items, or -1; also the guesses."""
    low = 0
    high = len(items) - 1
    guesses = 0
    while low <= high:
        middle = (low + high) // 2
        guesses = guesses + 1
        if items[middle] == target:
            return middle, guesses
        elif items[middle] < target:
            low = middle + 1          # target is in the right half
        else:
            high = middle - 1         # target is in the left half
    return -1, guesses


if __name__ == "__main__":
    numbers = list(range(1, 101))
    for target in [50, 37, 100, 1]:
        print(target, binary_search(numbers, target))
