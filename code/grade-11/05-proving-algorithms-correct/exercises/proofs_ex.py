"""Exercises of the chapter on proving algorithms correct."""


def largest_bug(t):                               # exercise 5
    best = t[0]
    for i in range(1, len(t) - 1):               # stops one place too early
        if t[i] > best:
            best = t[i]
    return best


def index_of_min(t, i):                           # exercise 7
    """Pre: 0 <= i < len(t). Post: m >= i and t[m] is a smallest element of t[i:]."""
    m = i
    for j in range(i + 1, len(t)):
        if t[j] < t[m]:
            m = j
    assert i <= m < len(t) and t[m] == min(t[i:])
    return m


def search_bug(t, x, cap=100):                    # exercise 8: hi = mid - 1
    lo, hi, turns = 0, len(t), 0
    while lo < hi and turns < cap:
        turns += 1
        mid = (lo + hi) // 2
        if t[mid] == x:
            return mid
        if t[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


def total(t):                                     # exercise 9
    s, i = 0, 0
    while i < len(t):
        assert s == sum(t[:i])
        s, i = s + t[i], i + 1
    return s


def count(t, x):                                  # exercise 10
    c = 0
    for i in range(len(t)):
        assert c == t[:i].count(x)
        if t[i] == x:
            c += 1
    return c


def is_sorted(t):                                 # exercise 11
    for i in range(1, len(t)):
        # invariant: t[:i] is sorted
        if t[i - 1] > t[i]:
            return False
    return True


def collatz_turns(n):                             # exercise 14
    turns = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        turns += 1
    return turns


def first_true(f, lo, hi):                        # exercise 15
    """Pre: f is False then True on lo..hi - 1 (never True then False).
    Post: the first k in lo..hi - 1 with f(k), or hi if there is none."""
    while lo < hi:
        # invariant: f is False on [old lo, lo) and True on [hi, old hi)
        mid = (lo + hi) // 2
        if f(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


if __name__ == "__main__":
    print(largest_bug([4, 9, 2, 11]), index_of_min([5, 3, 8, 1, 9], 0))
    t = [3, 8, 12, 15, 21, 30, 34, 41, 47, 52]
    print([x for x in t if search_bug(t, x) is None])
    print(total([4, 7, 1]), count([1, 2, 1, 1], 1), is_sorted([1, 2, 2, 5]))
    print(collatz_turns(27), first_true(lambda k: k * k > 50, 0, 100))
