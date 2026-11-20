// test-with: ../listings/heap.c ../exercises/kth.c ../exercises/median.c
// Random pushes and pops against a sorted array; heapify; the k-th smallest; the median.
#include "heap.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int kth_smallest(const int *xs, int n, int k);
typedef struct { heap low, high; } median;
void median_init(median *m);
void median_add(median *m, int x);
int median_get(const median *m);
void median_free(median *m);

static int by_value(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }
static unsigned s = 11;
static int rnd(int n) { return (int)((s = s * 1103515245u + 12345u) >> 8) % n; }

static void check_heap(const int *a, int n) {
    for (int i = 1; i < n; i++) assert(a[(i - 1) / 2] <= a[i]);
}

int main(void) {
    static int model[20000];
    int m = 0;
    heap h;
    heap_init(&h);
    for (int r = 0; r < 20000; r++) {
        if (m == 0 || rnd(3) > 0) {
            int x = rnd(1000);
            heap_push(&h, x);
            int j = m++;  // insert into the sorted model
            while (j > 0 && model[j - 1] > x) model[j] = model[j - 1], j--;
            model[j] = x;
        } else {
            assert(heap_pop(&h) == model[0]);
            memmove(model, model + 1, (size_t)--m * sizeof model[0]);
        }
        assert(h.n == m && (m == 0 || heap_min(&h) == model[0]));
    }
    check_heap(h.a, h.n);
    heap_free(&h);
    for (int n = 1; n <= 300; n++) {
        int a[300], b[300];
        for (int i = 0; i < n; i++) a[i] = b[i] = rnd(50);
        heapify(a, n);
        check_heap(a, n);
        qsort(b, (size_t)n, sizeof b[0], by_value);
        for (int k = 1; k <= n; k += 7) assert(kth_smallest(a, n, k) == b[k - 1]);
        median md;
        median_init(&md);
        int seen[300];
        for (int i = 0; i < n; i++) {
            median_add(&md, a[i]);
            seen[i] = a[i];
            qsort(seen, (size_t)i + 1, sizeof seen[0], by_value);
            assert(median_get(&md) == seen[i / 2]);
        }
        median_free(&md);
    }
    puts("heap: ok");
    return 0;
}
