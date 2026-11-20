// pq_naive.c: n insertions then n extract-min, counting the comparisons, for an unsorted
// array, a sorted array and a binary heap.
// capture: with=heap.c
#include "heap.h"
#include <stdio.h>
#include <stdlib.h>

static long cmp;

static long unsorted(const int *xs, int n) {
    int *a = malloc((size_t)n * sizeof *a), size = 0;
    cmp = 0;
    for (int i = 0; i < n; i++) a[size++] = xs[i];  // insert: O(1)
    while (size > 0) {                               // extract: scan for the minimum
        int m = 0;
        for (int j = 1; j < size; j++) cmp++, m = a[j] < a[m] ? j : m;
        a[m] = a[--size];
    }
    free(a);
    return cmp;
}

static long sorted(const int *xs, int n) {  // kept in decreasing order: the minimum is last
    int *a = malloc((size_t)n * sizeof *a), size = 0;
    cmp = 0;
    for (int i = 0; i < n; i++) {  // insert: shift the smaller elements right
        int j = size++;
        while (j > 0 && (cmp++, a[j - 1] < xs[i])) a[j] = a[j - 1], j--;
        a[j] = xs[i];
    }
    while (size > 0) size--;  // extract: O(1), no comparison
    free(a);
    return cmp;
}

static long binary_heap(const int *xs, int n) {
    heap h;
    heap_init(&h);
    heap_compares = 0;
    for (int i = 0; i < n; i++) heap_push(&h, xs[i]);
    while (h.n > 0) heap_pop(&h);
    heap_free(&h);
    return heap_compares;
}

int main(void) {
    printf("%6s %12s %12s %10s\n", "n", "unsorted", "sorted", "heap");
    unsigned s = 1;
    for (int n = 1000; n <= 64000; n *= 4) {
        int *xs = malloc((size_t)n * sizeof *xs);
        for (int i = 0; i < n; i++) xs[i] = (int)((s = s * 1103515245u + 12345u) >> 8);
        printf("%6d %12ld %12ld %10ld\n", n, unsorted(xs, n), sorted(xs, n), binary_heap(xs, n));
        free(xs);
    }
    return 0;
}
