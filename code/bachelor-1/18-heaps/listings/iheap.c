// iheap.c: every move of an item updates its position.
#include "iheap.h"
#include <stdlib.h>

static void place(iheap *h, int i, int x) {
    h->item[i] = x;
    h->pos[x] = i;
}

static void up(iheap *h, int i) {
    int x = h->item[i];
    while (i > 0 && h->key[h->item[(i - 1) / 2]] > h->key[x]) {
        place(h, i, h->item[(i - 1) / 2]);  // the parent moves down
        i = (i - 1) / 2;
    }
    place(h, i, x);
}

static void down(iheap *h, int i) {
    int x = h->item[i];
    for (int c; (c = 2 * i + 1) < h->n; i = c) {
        if (c + 1 < h->n && h->key[h->item[c + 1]] < h->key[h->item[c]]) c++;
        if (h->key[x] <= h->key[h->item[c]]) break;
        place(h, i, h->item[c]);  // the smaller child moves up
    }
    place(h, i, x);
}

void ih_init(iheap *h, int cap) {
    *h = (iheap){malloc((size_t)cap * sizeof(int)), malloc((size_t)cap * sizeof(int)),
                 malloc((size_t)cap * sizeof(int)), 0, cap};
    if (h->item == NULL || h->pos == NULL || h->key == NULL) exit(1);
    for (int x = 0; x < cap; x++) h->pos[x] = -1;
}

void ih_push(iheap *h, int x, int key) {
    h->key[x] = key;
    place(h, h->n++, x);
    up(h, h->n - 1);
}

bool ih_contains(const iheap *h, int x) { return h->pos[x] >= 0; }

void ih_decrease(iheap *h, int x, int key) {
    h->key[x] = key;
    up(h, h->pos[x]);  // a smaller key can only move up
}

int ih_pop(iheap *h) {
    int top = h->item[0];
    h->pos[top] = -1;
    if (--h->n > 0) {
        place(h, 0, h->item[h->n]);
        down(h, 0);
    }
    return top;
}

void ih_free(iheap *h) {
    free(h->item);
    free(h->pos);
    free(h->key);
}
