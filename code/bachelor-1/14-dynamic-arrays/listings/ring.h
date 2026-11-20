// ring.h: a queue of int in a circular buffer that grows when full.
#ifndef RING_H
#define RING_H
#include <stddef.h>

typedef struct ring ring;

ring *ring_new(size_t capacity);  // constructor; precondition: capacity >= 1
void ring_free(ring *r);
size_t ring_size(const ring *r);
void ring_put(ring *r, int x);    // add x at the back
int ring_take(ring *r);           // remove the front; precondition: size > 0
void ring_show(const ring *r);    // print the cells, the front marked by [ ]
#endif
