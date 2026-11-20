// build.c: swaps made by building a min-heap of n keys, bottom-up (heapify) and top-down
// (n insertions), on decreasing keys, the worst case for both.
// capture: with=heap.c
#include "heap.h"
#include <stdio.h>
#include <stdlib.h>

static int ones(int n) { return n == 0 ? 0 : (n & 1) + ones(n >> 1); }

int main(void) {
    printf("%7s %10s %8s %12s %10s\n", "n", "bottom-up", "n-v(n)", "top-down", "per key");
    for (int n = 1023; n <= 1048575; n = 4 * n + 3) {
        int *a = malloc((size_t)n * sizeof *a);
        for (int i = 0; i < n; i++) a[i] = n - i;
        heap_swaps = 0;
        heapify(a, n);
        long bottom = heap_swaps;
        for (int i = 0; i < n; i++) a[i] = n - i;
        heap_swaps = 0;
        for (int i = 1; i < n; i++) sift_up(a, i);  // a[0..i) is already a heap
        printf("%7d %10ld %8d %12ld %10.2f\n", n, bottom, n - ones(n), heap_swaps,
               (double)heap_swaps / n);
        free(a);
    }
    return 0;
}
