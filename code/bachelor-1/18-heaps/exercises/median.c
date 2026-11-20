// median.c: the running median of a stream: a max-heap of the lower half (negated values)
// and a min-heap of the upper half, of equal sizes or the lower one larger by one.
#include "heap.h"

typedef struct {
    heap low, high;
} median;

void median_init(median *m) { heap_init(&m->low), heap_init(&m->high); }

void median_add(median *m, int x) {
    if (m->low.n == 0 || x <= -heap_min(&m->low)) heap_push(&m->low, -x);
    else heap_push(&m->high, x);
    if (m->low.n > m->high.n + 1) heap_push(&m->high, -heap_pop(&m->low));  // rebalance
    else if (m->high.n > m->low.n) heap_push(&m->low, -heap_pop(&m->high));
}

int median_get(const median *m) { return -heap_min(&m->low); }  // the lower median

void median_free(median *m) { heap_free(&m->low), heap_free(&m->high); }
