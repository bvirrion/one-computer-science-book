// heap.c: the parent of i is (i - 1) / 2, its children 2i + 1 and 2i + 2.
#include "heap.h"
#include <stdlib.h>

long heap_swaps, heap_compares;

static void swap(int *a, int i, int j) {
    int t = a[i];
    a[i] = a[j], a[j] = t;
    heap_swaps++;
}

void sift_up(int *a, int i) {
    while (i > 0) {
        int p = (i - 1) / 2;
        heap_compares++;
        if (a[p] <= a[i]) return;  // the heap property holds at i
        swap(a, i, p);
        i = p;  // now only p may be smaller than its parent
    }
}

void sift_down(int *a, int n, int i) {
    for (;;) {
        int c = 2 * i + 1;  // the left child
        if (c >= n) return;
        if (c + 1 < n && (heap_compares++, a[c + 1] < a[c])) c++;  // the smaller child
        heap_compares++;
        if (a[i] <= a[c]) return;
        swap(a, i, c);
        i = c;  // now only c may be larger than its children
    }
}

void heapify(int *a, int n) {
    for (int i = n / 2 - 1; i >= 0; i--) sift_down(a, n, i);  // from the last parent up
}

void heap_init(heap *h) { *h = (heap){NULL, 0, 0}; }

void heap_push(heap *h, int x) {
    if (h->n == h->cap) {
        h->cap = h->cap ? 2 * h->cap : 8;
        h->a = realloc(h->a, (size_t)h->cap * sizeof *h->a);
        if (h->a == NULL) exit(1);
    }
    h->a[h->n] = x;  // a new leaf at the end of the last level
    sift_up(h->a, h->n++);
}

int heap_min(const heap *h) { return h->a[0]; }

int heap_pop(heap *h) {
    int top = h->a[0];
    h->a[0] = h->a[--h->n];  // the last leaf moves to the root
    sift_down(h->a, h->n, 0);
    return top;
}

void heap_free(heap *h) { free(h->a); }
