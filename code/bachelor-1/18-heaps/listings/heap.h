// heap.h: a binary min-heap of ints in a growing array, and its two sifting operations.
#ifndef HEAP_H
#define HEAP_H

typedef struct {
    int *a;      // a[0..n) satisfies the heap property
    int n, cap;
} heap;

extern long heap_swaps, heap_compares;  // counted by the sifting operations

void sift_up(int *a, int i);            // a[0..i] is a heap except at i
void sift_down(int *a, int n, int i);   // a[0..n) is a heap except at i
void heapify(int *a, int n);            // bottom-up construction

void heap_init(heap *h);
void heap_push(heap *h, int x);
int heap_min(const heap *h);            // precondition: n > 0
int heap_pop(heap *h);                  // removes and returns the minimum; n > 0
void heap_free(heap *h);
#endif
