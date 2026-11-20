# pysieve.py: the same sieve, line for line, run by the Python interpreter.
import time

N = 20_000_000


def count_primes(n):
    composite = bytearray(n)
    count = 0
    for i in range(2, n):
        if composite[i]:
            continue
        count += 1
        for j in range(i * i, n, i):
            composite[j] = 1
    return count


if __name__ == "__main__":
    t0 = time.perf_counter()
    count = count_primes(N)
    t1 = time.perf_counter()
    print(f"primes below {N}: {count}")
    print(f"time: {t1 - t0:.2f} s")
