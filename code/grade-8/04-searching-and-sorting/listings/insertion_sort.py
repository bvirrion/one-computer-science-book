def insertion_sort(items):
    """Sort items in place, smallest first; return the number of comparisons."""
    comparisons = 0
    for i in range(1, len(items)):
        j = i
        moving = True
        while moving and j > 0:
            comparisons = comparisons + 1
            if items[j - 1] > items[j]:
                items[j - 1], items[j] = items[j], items[j - 1]   # swap the two
                j = j - 1
            else:
                moving = False         # in its place among the sorted ones
    return comparisons


if __name__ == "__main__":
    cards = [7, 3, 9, 1, 8, 4]
    print(insertion_sort(cards), "comparisons:", cards)
