from sieve import sieve

primes = sieve(101)
for row in range(10):
    line = ""
    for col in range(1, 11):
        k = row * 10 + col
        if k in primes:
            line = line + f"{k:>4}"
        else:
            line = line + "   ."
    print(line)
