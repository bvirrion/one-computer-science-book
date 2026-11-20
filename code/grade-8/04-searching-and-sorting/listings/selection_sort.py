def selection_sort(items):
    """Sort items in place, smallest first; return the number of comparisons."""
    comparisons = 0
    for start in range(len(items) - 1):
        smallest = start
        for i in range(start + 1, len(items)):
            comparisons = comparisons + 1
            if items[i] < items[smallest]:
                smallest = i
        items[start], items[smallest] = items[smallest], items[start]   # swap the two
    return comparisons


if __name__ == "__main__":
    cards = [7, 3, 9, 1, 8, 4]
    print(selection_sort(cards), "comparisons:", cards)
