// topk.c: keep the k best hits seen; a new hit only has to beat the worst kept.
#include "topk.h"

#include <stdlib.h>

int hit_better(Hit a, Hit b) {
    return a.score > b.score || (a.score == b.score && a.doc < b.doc);
}

void topk_init(TopK *t, Hit *storage, int k) {
    *t = (TopK){storage, 0, k};
}

static void swap(Hit *a, Hit *b) {
    Hit tmp = *a;
    *a = *b;
    *b = tmp;
}

static void sift_down(TopK *t, int i) {
    for (;;) {
        int worst = i, l = 2 * i + 1, r = l + 1;
        if (l < t->size && hit_better(t->heap[worst], t->heap[l]))
            worst = l;
        if (r < t->size && hit_better(t->heap[worst], t->heap[r]))
            worst = r;
        if (worst == i)
            return;
        swap(&t->heap[i], &t->heap[worst]);
        i = worst;
    }
}

void topk_push(TopK *t, Hit h) {
    if (t->size < t->k) {  // room left: add at the bottom and sift up
        int i = t->size++;
        t->heap[i] = h;
        while (i > 0 && hit_better(t->heap[(i - 1) / 2], t->heap[i])) {
            swap(&t->heap[i], &t->heap[(i - 1) / 2]);
            i = (i - 1) / 2;
        }
    } else if (t->k > 0 && hit_better(h, t->heap[0])) {  // it beats the worst kept
        t->heap[0] = h;
        sift_down(t, 0);
    }
}

static int best_first(const void *a, const void *b) {
    return hit_better(*(const Hit *)b, *(const Hit *)a) - hit_better(*(const Hit *)a,
                                                                       *(const Hit *)b);
}

int topk_sorted(TopK *t) {
    qsort(t->heap, t->size, sizeof *t->heap, best_first);
    return t->size;
}
