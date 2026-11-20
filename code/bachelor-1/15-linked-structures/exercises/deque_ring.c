// deque_ring.c: a deque on a circular buffer of fixed capacity.
#include <stdbool.h>
#include <stddef.h>

enum { CAP = 8 };

typedef struct {
    int data[CAP];
    size_t head, count;  // the deque is data[head], ..., data[(head + count - 1) % CAP]
} deque;

void deque_init(deque *d) { d->head = d->count = 0; }
bool deque_full(const deque *d) { return d->count == CAP; }
void deque_push_back(deque *d, int x) { d->data[(d->head + d->count++) % CAP] = x; }

void deque_push_front(deque *d, int x) {
    d->head = (d->head + CAP - 1) % CAP;  // one step back, without going negative
    d->data[d->head] = x;
    d->count++;
}

int deque_pop_front(deque *d) {
    int x = d->data[d->head];
    d->head = (d->head + 1) % CAP;
    d->count--;
    return x;
}

int deque_pop_back(deque *d) { return d->data[(d->head + --d->count) % CAP]; }
