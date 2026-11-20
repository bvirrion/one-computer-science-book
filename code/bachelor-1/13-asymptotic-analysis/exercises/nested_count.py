"""nested_count.py: the triples i < j < k, counted by the loops and by a formula."""


def count_triples(n):
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            for _k in range(j + 1, n):
                count += 1
    return count


def closed_form(n):
    return n * (n - 1) * (n - 2) // 6
