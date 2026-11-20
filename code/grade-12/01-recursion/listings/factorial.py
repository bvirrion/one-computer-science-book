def factorial(n):
    """n! = 1 x 2 x ... x n, for a whole number n >= 0."""
    if n == 0:                       # base case
        return 1
    return n * factorial(n - 1)      # recursive case


def sum_list(t):
    """The sum of the numbers of the list t."""
    if t == []:
        return 0
    return t[0] + sum_list(t[1:])


def power(x, n):
    """x to the power n, for a whole number n >= 0."""
    if n == 0:
        return 1
    return x * power(x, n - 1)


if __name__ == "__main__":
    print([factorial(n) for n in range(8)])
    print(factorial(25))
    print(sum_list([3, 1, 4, 1, 5]), power(2, 10))
