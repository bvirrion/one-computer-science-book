"""Exercises of the chapter on recursion."""


def reverse(s):                                   # exercise 3
    if s == "":
        return ""
    return reverse(s[1:]) + s[0]


def count_digits(n):                              # exercise 5
    """The number of decimal digits of the whole number n >= 0."""
    if n < 10:
        return 1
    return 1 + count_digits(n // 10)


def factorial_checked(n):                         # exercise 7
    if n < 0:
        raise ValueError("factorial of a negative number")
    if n == 0:
        return 1
    return n * factorial_checked(n - 1)


def flatten(nested):                              # exercise 8
    if not isinstance(nested, list):
        return [nested]
    out = []
    for item in nested:
        out += flatten(item)
    return out


def show(n, printed):                             # exercise 10
    if n == 0:
        return
    show(n - 1, printed)
    printed.append(n)
    show(n - 1, printed)


def is_palindrome(s):                             # exercise 11
    if len(s) <= 1:
        return True
    return s[0] == s[-1] and is_palindrome(s[1:-1])


def fib_calls(n):                                 # exercise 13: calls made by fib(n)
    return 1 if n < 2 else 1 + fib_calls(n - 1) + fib_calls(n - 2)


def subsets(t):                                   # exercise 14
    if t == []:
        return [[]]
    rest = subsets(t[1:])
    return rest + [[t[0]] + s for s in rest]


def binary(n):                                    # exercise 15
    """The binary writing of the whole number n >= 0, as a string."""
    if n < 2:
        return str(n)
    return binary(n // 2) + str(n % 2)


if __name__ == "__main__":
    printed = []
    show(3, printed)
    print(reverse("loop"), count_digits(2026), printed)
    print(flatten([1, [2, [3, 4]], [], 5]))
    print(is_palindrome("kayak"), fib_calls(5), subsets([1, 2, 3]))
    print(binary(37))
