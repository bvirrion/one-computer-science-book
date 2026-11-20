from functools import cache


@cache                                  # Python keeps the notebook for us
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(fib(90))
print(fib.cache_info())
