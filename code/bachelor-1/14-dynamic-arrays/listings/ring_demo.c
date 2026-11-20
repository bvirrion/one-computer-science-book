// ring_demo.c: a queue that wraps around its array, then grows.
// capture: with=ring.c
#include "ring.h"
#include <stdio.h>

int main(void) {
    ring *r = ring_new(5);
    for (int x = 1; x <= 4; x++) ring_put(r, x);
    printf("put 1..4     ");
    ring_show(r);
    int a = ring_take(r);
    int b = ring_take(r);
    printf("take %d, %d   ", a, b);
    ring_show(r);
    ring_put(r, 5);
    ring_put(r, 6);
    printf("put 5, 6     ");
    ring_show(r);
    ring_put(r, 7);
    printf("put 7        ");
    ring_show(r);
    ring_put(r, 8);
    printf("put 8 (grow) ");
    ring_show(r);
    ring_free(r);
    return 0;
}
