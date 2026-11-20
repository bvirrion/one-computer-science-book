"""reverse_twice.py: reversing a list twice, defined by recursion on lists."""

from itertools import product


def rev(xs):
    """rev([]) = [];  rev([x] + rest) = rev(rest) + [x]."""
    return [] if not xs else rev(xs[1:]) + [xs[0]]


if __name__ == "__main__":
    print(rev([1, 2, 3, 4]), rev(rev([1, 2, 3, 4])))
    checked = 0
    for n in range(8):
        for xs in product(range(3), repeat=n):  # every list of length n over {0, 1, 2}
            xs = list(xs)
            assert rev(rev(xs)) == xs
            assert all(rev(xs[:k] + xs[k:]) == rev(xs[k:]) + rev(xs[:k])
                       for k in range(n + 1))
            checked += 1
    print(checked, "lists checked; a check is not a proof: see the induction")
