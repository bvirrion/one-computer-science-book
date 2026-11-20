"""even_odd.py: mutual recursion; the variant n decreases at every call."""


def is_even(n):
    return True if n == 0 else is_odd(n - 1)


def is_odd(n):
    return False if n == 0 else is_even(n - 1)


if __name__ == "__main__":
    print([n for n in range(12) if is_even(n)], is_odd(7))
