// test-with: ../listings/ring.c
// The ring buffer against a plain array used as a queue.
#include "ring.h"
#include <assert.h>
#include <stdio.h>

int main(void) {
    ring *r = ring_new(1);
    static int model[100000];
    size_t front = 0, back = 0;
    unsigned state = 7;
    for (int i = 0; i < 100000; i++) {
        state = state * 1103515245u + 12345u;
        if (back == front || (state >> 16) % 3 != 0) {
            ring_put(r, i);
            model[back++] = i;
        } else {
            assert(ring_take(r) == model[front++]);
        }
        assert(ring_size(r) == back - front);
    }
    while (front < back) assert(ring_take(r) == model[front++]);
    ring_free(r);
    puts("ring: ok");
    return 0;
}
