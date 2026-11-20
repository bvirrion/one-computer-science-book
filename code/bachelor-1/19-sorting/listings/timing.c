// timing.c: milliseconds to sort a million random ints below 10^9, best of three runs.
// capture: with=sorts.c,radix.c
#define _POSIX_C_SOURCE 199309L
#include "radix.h"
#include "sorts.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

enum { N = 1000000 };
static int data[N], a[N];

static int up(const void *x, const void *y) {
    int p = *(const int *)x, q = *(const int *)y;
    return (p > q) - (p < q);
}
static void c_qsort(int *v, int n) { qsort(v, (size_t)n, sizeof *v, up); }
static void radix9(int *v, int n) { radix_sort(v, n, 9); }

static double best_ms(void (*sort)(int *, int)) {
    double best = 1e9;
    for (int r = 0; r < 3; r++) {
        memcpy(a, data, sizeof a);
        struct timespec t0, t1;
        clock_gettime(CLOCK_MONOTONIC, &t0);
        sort(a, N);
        clock_gettime(CLOCK_MONOTONIC, &t1);
        double ms = (t1.tv_sec - t0.tv_sec) * 1e3 + (t1.tv_nsec - t0.tv_nsec) * 1e-6;
        best = ms < best ? ms : best;
        for (int i = 1; i < N; i++)
            if (a[i - 1] > a[i]) return -1;
    }
    return best;
}

int main(void) {
    unsigned s = 7;
    for (int i = 0; i < N; i++) data[i] = (int)((s = s * 1103515245u + 12345u) % 1000000000u);
    const char *names[] = {"qsort (C library)", "quicksort", "merge sort", "heapsort",
                           "radix sort"};
    void (*sorts[])(int *, int) = {c_qsort, quicksort, merge_sort, heap_sort, radix9};
    for (int k = 0; k < 5; k++) printf("%-18s %7.1f ms\n", names[k], best_ms(sorts[k]));
    return 0;
}
