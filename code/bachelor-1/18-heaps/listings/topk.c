// topk.c: the k longest loans, in one pass, with a min-heap of the k longest seen so far.
// capture: with=heap.c
#include "heap.h"
#include "loans.h"

int main(void) {
    read_loans();
    int k = 8, returned = 0;
    heap h;  // its root is the shortest of the k kept: the one to beat
    heap_init(&h);
    for (int i = 0; i < LOANS; i++) {
        if (loans[i].returned < 0) continue;
        int days = loans[i].returned - loans[i].out;
        returned++;
        if (h.n < k) heap_push(&h, days);
        else if (days > heap_min(&h)) {  // longer than the shortest kept: replace it
            h.a[0] = days;
            sift_down(h.a, h.n, 0);
        }
    }
    printf("%d returned loans; the %d longest, in days:", returned, k);
    while (h.n > 0) printf(" %d", heap_pop(&h));
    printf("\n");
    heap_free(&h);
    return 0;
}
