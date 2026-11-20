def h(n):
    """The number of times n can be halved (rounding down) before it reaches 1."""
    count = 0
    while n > 1:
        n = n // 2
        count += 1
    return count


print("         n   h(n)   2^h(n) <= n < 2^(h(n)+1)")
for n in [1, 2, 3, 7, 8, 1000, 10**6, 10**9]:
    k = h(n)
    assert 2**k <= n < 2**(k + 1)
    print(f"{n:10} {k:6}   {2**k:>10} <= n < {2**(k + 1)}")
