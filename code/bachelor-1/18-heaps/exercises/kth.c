// kth.c: the k-th smallest of n values, with a max-heap of the k smallest seen: O(n log k).
#include "heap.h"

int kth_smallest(const int *xs, int n, int k) {  // 1 <= k <= n
    heap h;  // negated values: its root is minus the largest of the k kept
    heap_init(&h);
    for (int i = 0; i < n; i++)
        if (h.n < k) heap_push(&h, -xs[i]);
        else if (xs[i] < -heap_min(&h)) {
            h.a[0] = -xs[i];
            sift_down(h.a, h.n, 0);
        }
    int answer = -heap_min(&h);
    heap_free(&h);
    return answer;
}
