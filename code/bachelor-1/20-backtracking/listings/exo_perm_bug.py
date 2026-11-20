"""exo_perm_bug.py: exercise 5, permutations by swapping, without the undo."""


def permutations(a, k=0):
    if k == len(a):
        yield "".join(a)
        return
    for i in range(k, len(a)):
        a[k], a[i] = a[i], a[k]
        yield from permutations(a, k + 1)


if __name__ == "__main__":
    out = list(permutations(list("abc")))
    print(out, len(set(out)), "distinct")
