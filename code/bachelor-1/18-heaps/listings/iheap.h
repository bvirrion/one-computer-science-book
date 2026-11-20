// iheap.h: a min-heap of items 0..cap-1 with keys, which knows where each item sits,
// so that the key of an item can be decreased.
#ifndef IHEAP_H
#define IHEAP_H
#include <stdbool.h>

typedef struct {
    int *item;  // item[0..n): the heap, ordered by key[item[i]]
    int *pos;   // pos[x]: the index of item x in the heap, or -1
    int *key;
    int n, cap;
} iheap;

void ih_init(iheap *h, int cap);
void ih_push(iheap *h, int x, int key);  // precondition: x not in the heap
bool ih_contains(const iheap *h, int x);
void ih_decrease(iheap *h, int x, int key);  // precondition: key <= the key of x
int ih_pop(iheap *h);  // the item of smallest key; precondition: n > 0
void ih_free(iheap *h);
#endif
