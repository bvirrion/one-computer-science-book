from factorial import factorial, sum_list


def factorial_loop(n):
    result = 1
    for k in range(1, n + 1):        # the multiplications the recursion does, in order
        result *= k
    return result


def sum_loop(t):
    total = 0
    for x in t:
        total += x
    return total


print(all(factorial(n) == factorial_loop(n) for n in range(100)))
print(sum_list(list(range(500))) == sum_loop(range(500)))
print(factorial_loop(3000) > 10**9000, "| factorial(3000) by recursion:", end=" ")
try:
    factorial(3000)
except RecursionError:
    print("RecursionError")
