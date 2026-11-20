/* ex5_sum.c -- the fixed parallel sum: each thread sums its own slice into its own
   partial, and the main thread adds the p partials after joining. */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { const int *a; size_t lo, hi; long partial; } slice;

static void *sum_slice(void *arg)
{
    slice *s = arg;
    long t = 0; /* a local: no other thread can see it */
    for (size_t i = s->lo; i < s->hi; i++) t += s->a[i];
    s->partial = t;
    return NULL;
}

long par_sum(const int *a, size_t n, int p)
{
    pthread_t t[64];
    slice s[64];
    for (int k = 0; k < p; k++) {
        s[k] = (slice){a, n * k / p, n * (k + 1) / p, 0};
        pthread_create(&t[k], NULL, sum_slice, &s[k]);
    }
    long total = 0;
    for (int k = 0; k < p; k++) {
        pthread_join(t[k], NULL);
        total += s[k].partial;
    }
    return total;
}

int main(void)
{
    size_t n = 1000000;
    int *a = malloc(n * sizeof *a);
    for (size_t i = 0; i < n; i++) a[i] = (int)(i % 1000);
    for (int p = 1; p <= 8; p++) printf("p = %d: %ld\n", p, par_sum(a, n, p));
    free(a);
    return 0;
}
