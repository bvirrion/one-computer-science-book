from insertion_sort import insertion_sort
from selection_sort import selection_sort


def mixed(n):
    """The numbers 0 to n - 1 in a fixed mixed order: the remainders of 37 x i by n."""
    items = []
    for i in range(n):
        items.append((37 * i) % n)
    return items


if __name__ == "__main__":
    print("n      order      selection  insertion")
    for n in [10, 100, 1000]:
        for name in ["sorted", "reversed", "mixed"]:
            if name == "sorted":
                items = list(range(n))
            elif name == "reversed":
                items = list(range(n, 0, -1))
            else:
                items = mixed(n)
            by_selection = selection_sort(list(items))
            by_insertion = insertion_sort(list(items))
            print(f"{n:<6} {name:<10} {by_selection:>9} {by_insertion:>10}")
