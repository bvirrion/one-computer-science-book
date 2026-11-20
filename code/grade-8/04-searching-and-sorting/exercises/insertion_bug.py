def insertion_sort(items):
    for i in range(2, len(items)):
        j = i
        while j > 0 and items[j - 1] > items[j]:
            items[j - 1], items[j] = items[j], items[j - 1]
            j = j - 1


cards = [5, 1, 3]
insertion_sort(cards)
print(cards)
