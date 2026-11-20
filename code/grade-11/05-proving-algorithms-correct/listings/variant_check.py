def gcd(a, b):
    """Euclid; pre: a >= 0, b >= 0. Variant: b, a whole number that decreases."""
    turn = 0
    while b != 0:
        print(f"turn {turn:2}: a={a:4} b={b:4}")
        a, b = b, a % b       # the new b is a % b, which is smaller than b
        turn = turn + 1
    print(f"turn {turn:2}: a={a:4} b={b:4}  -> b = 0, the loop stops")
    return a


print("gcd =", gcd(1071, 462))
print("gcd =", gcd(233, 144))
