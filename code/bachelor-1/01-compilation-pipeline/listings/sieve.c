// sieve.c: count the primes below N with the sieve of Eratosthenes, and time it.
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

enum { N = 20000000 };

int main(void)
{
    struct timespec t0, t1;
    timespec_get(&t0, TIME_UTC);
    char *composite = calloc(N, 1);
    if (composite == NULL)
        return 1;
    long count = 0;
    for (long i = 2; i < N; i++) {
        if (composite[i])
            continue;
        count++;
        for (long j = i * i; j < N; j += i)
            composite[j] = 1;
    }
    free(composite);
    timespec_get(&t1, TIME_UTC);
    double s = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;
    printf("primes below %d: %ld\n", N, count);
    printf("time: %.2f s\n", s);
    return 0;
}
