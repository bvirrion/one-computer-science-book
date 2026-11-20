/* psort.c -- merge sort of 2^24 integers, the two halves of each of the top
   log2(p) levels sorted by two threads, p = 1, 2, 4, 8; every merge is sequential.
   Best of three runs. */
#define _POSIX_C_SOURCE 199309L
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct { int *a, *tmp; size_t n; int threads; } job;

static void merge(int *a, int *tmp, size_t n)
{
    size_t h = n / 2, i = 0, j = h, k = 0;
    while (i < h && j < n) tmp[k++] = a[i] <= a[j] ? a[i++] : a[j++];
    while (i < h) tmp[k++] = a[i++];
    while (j < n) tmp[k++] = a[j++];
    memcpy(a, tmp, n * sizeof *a);
}

static void *sort(void *arg)
{
    job *w = arg;
    if (w->n < 2) return NULL;
    size_t h = w->n / 2;
    job left = {w->a, w->tmp, h, w->threads / 2};
    job right = {w->a + h, w->tmp + h, w->n - h, w->threads - w->threads / 2};
    if (w->threads > 1) { /* fork: the left half on a new thread, the right here */
        pthread_t t;
        pthread_create(&t, NULL, sort, &left);
        sort(&right);
        pthread_join(t, NULL); /* join */
    } else {
        sort(&left);
        sort(&right);
    }
    merge(w->a, w->tmp, w->n);
    return NULL;
}

static double now_ms(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec / 1e6;
}

int main(void)
{
    size_t n = (size_t)1 << 24;
    int *src = malloc(n * sizeof *src), *a = malloc(n * sizeof *a), *tmp = malloc(n * sizeof *a);
    unsigned x = 12345;
    for (size_t i = 0; i < n; i++) { x = x * 1103515245u + 12345u; src[i] = (int)(x >> 1); }
    double base = 0;
    printf(" p  time ms  speed-up\n");
    for (int p = 1; p <= 8; p *= 2) {
        double best = 1e300;
        for (int run = 0; run < 3; run++) {
            memcpy(a, src, n * sizeof *a);
            double t0 = now_ms();
            job all = {a, tmp, n, p};
            sort(&all);
            double t = now_ms() - t0;
            if (t < best) best = t;
            for (size_t i = 1; i < n; i++)
                if (a[i - 1] > a[i]) { printf("not sorted\n"); return 1; }
        }
        if (p == 1) base = best;
        printf("%2d %8.1f %9.2f\n", p, best, base / best);
    }
    free(src); free(a); free(tmp);
    return 0;
}
