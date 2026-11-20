// heap_demo.c: the array of a min-heap after each insertion and each extraction.
// capture: with=heap.c
#include "heap.h"
#include <stdio.h>

static void show(const char *what, const heap *h) {
    printf("%-10s [", what);
    for (int i = 0; i < h->n; i++) printf(i ? " %d" : "%d", h->a[i]);
    printf("]\n");
}

int main(void) {
    heap h;
    heap_init(&h);
    int xs[] = {7, 4, 9, 1, 8, 3, 2};
    char what[16];
    for (int i = 0; i < 7; i++) {
        heap_push(&h, xs[i]);
        snprintf(what, sizeof what, "push %d", xs[i]);
        show(what, &h);
    }
    for (int i = 0; i < 3; i++) {
        int m = heap_pop(&h);
        snprintf(what, sizeof what, "pop -> %d", m);
        show(what, &h);
    }
    heap_free(&h);
    return 0;
}
