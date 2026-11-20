// ring.c: the circular buffer: a head index and a count, indices taken modulo capacity.
#include "ring.h"
#include <stdio.h>
#include <stdlib.h>

struct ring {
    int *data;
    size_t head, count, capacity;
};
// invariant: count <= capacity; the queue is data[head], data[(head + 1) % capacity],
// ..., data[(head + count - 1) % capacity], front first

static void *checked(void *p) {
    if (p == NULL) {
        perror("ring");
        exit(1);
    }
    return p;
}

ring *ring_new(size_t capacity) {
    ring *r = checked(malloc(sizeof *r));
    *r = (ring){checked(calloc(capacity, sizeof(int))), 0, 0, capacity};
    return r;
}

void ring_free(ring *r) {
    free(r->data);
    free(r);
}

size_t ring_size(const ring *r) { return r->count; }

void ring_put(ring *r, int x) {
    if (r->count == r->capacity) {  // full: copy in queue order into twice the room
        int *data = checked(calloc(2 * r->capacity, sizeof(int)));
        for (size_t i = 0; i < r->count; i++)
            data[i] = r->data[(r->head + i) % r->capacity];
        free(r->data);
        *r = (ring){data, 0, r->count, 2 * r->capacity};
    }
    r->data[(r->head + r->count) % r->capacity] = x;
    r->count++;
}

int ring_take(ring *r) {
    int x = r->data[r->head];
    r->head = (r->head + 1) % r->capacity;
    r->count--;
    return x;
}

void ring_show(const ring *r) {
    for (size_t i = 0; i < r->capacity; i++) {
        size_t k = (i + r->capacity - r->head) % r->capacity;  // position in the queue
        if (k >= r->count) printf("  . ");
        else if (k == 0) printf("[%2d]", r->data[i]);
        else printf(" %2d ", r->data[i]);
    }
    printf("   size %zu\n", r->count);
}
