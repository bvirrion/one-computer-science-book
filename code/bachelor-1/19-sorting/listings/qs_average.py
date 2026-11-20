"""qs_average.py: the exact average number of comparisons of quicksort (Lomuto, last
element as pivot) over all n! orders of n distinct keys, against 2(n+1)H_n - 4n."""

from fractions import Fraction
from itertools import permutations


def comparisons(a):
    """Comparisons made by quicksort on the list a (sorted in place)."""
    count, stack = 0, [(0, len(a))]
    while stack:
        lo, hi = stack.pop()
        if hi - lo < 2:
            continue
        p, k = a[hi - 1], lo
        for j in range(lo, hi - 1):
            count += 1
            if a[j] < p:
                a[k], a[j] = a[j], a[k]
                k += 1
        a[k], a[hi - 1] = a[hi - 1], a[k]
        stack += [(lo, k), (k + 1, hi)]
    return count


def formula(n):
    harmonic = sum(Fraction(1, k) for k in range(1, n + 1))
    return 2 * (n + 1) * harmonic - 4 * n


def exact_average(n):
    orders = list(permutations(range(n)))
    return Fraction(sum(comparisons(list(p)) for p in orders), len(orders))


def main():
    print(f"{'n':>2} {'n!':>6} {'average':>10} {'2(n+1)H_n - 4n':>15}  worst")
    for n in range(1, 9):
        avg = exact_average(n)
        worst = max(comparisons(list(p)) for p in permutations(range(n)))
        print(f"{n:2} {len(list(permutations(range(n)))):6} {str(avg):>10} "
              f"{str(formula(n)):>15}  {worst}")


if __name__ == "__main__":
    main()
