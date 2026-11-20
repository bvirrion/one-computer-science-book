// counts.c: key comparisons of the sorts, against the lower bound ceil(lg n!).
// Shuffled: the average over 200 random orders of 0..n-1.
// capture: with=sorts.c
#include "sorts.h"
#include <math.h>
#include <stdio.h>

static unsigned s = 19;
static double average(void (*sort)(int *, int), int n, int shuffled) {
    int a[64];
    long total = 0;
    int runs = shuffled ? 200 : 1;
    for (int r = 0; r < runs; r++) {
        for (int i = 0; i < n; i++) a[i] = i;
        for (int i = n - 1; shuffled && i > 0; i--) {
            int j = (int)((s = s * 1103515245u + 12345u) >> 8) % (i + 1), t = a[i];
            a[i] = a[j], a[j] = t;
        }
        sort_compares = 0;
        sort(a, n);
        total += sort_compares;
    }
    return (double)total / runs;
}

int main(void) {
    printf("%3s %10s %10s %8s %8s %8s %8s\n", "n", "qs sorted", "qs random", "qs+", "merge",
           "heap", "bound");
    for (int n = 4; n <= 64; n += 4) {
        double lg_fact = 0;
        for (int k = 2; k <= n; k++) lg_fact += log2(k);
        printf("%3d %10.0f %10.1f %8.1f %8.1f %8.1f %8.0f\n", n, average(quicksort_basic, n, 0),
               average(quicksort_basic, n, 1), average(quicksort, n, 1), average(merge_sort, n, 1),
               average(heap_sort, n, 1), ceil(lg_fact - 1e-9));
    }
    return 0;
}
