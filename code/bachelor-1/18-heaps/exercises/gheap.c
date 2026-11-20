// gheap.c: a max-heap of any element type, ordered by a comparison function.
#include <stdlib.h>
#include <string.h>

typedef int (*compare)(const void *, const void *);
typedef struct {
    char *a;  // n elements of `size` bytes
    size_t n, cap, size;
    compare cmp;
} gheap;

static void *at(const gheap *h, size_t i) { return h->a + i * h->size; }

static void swap(gheap *h, size_t i, size_t j) {
    char t[64];  // elements of at most 64 bytes
    memcpy(t, at(h, i), h->size);
    memcpy(at(h, i), at(h, j), h->size);
    memcpy(at(h, j), t, h->size);
}

void gheap_init(gheap *h, size_t size, compare cmp) { *h = (gheap){NULL, 0, 0, size, cmp}; }

void gheap_push(gheap *h, const void *x) {
    if (h->n == h->cap) {
        h->cap = h->cap ? 2 * h->cap : 8;
        h->a = realloc(h->a, h->cap * h->size);
        if (h->a == NULL) exit(1);
    }
    memcpy(at(h, h->n), x, h->size);
    for (size_t i = h->n++; i > 0 && h->cmp(at(h, (i - 1) / 2), at(h, i)) < 0; i = (i - 1) / 2)
        swap(h, i, (i - 1) / 2);
}

void gheap_pop(gheap *h, void *out) {  // the largest element, copied to out; n > 0
    memcpy(out, at(h, 0), h->size);
    memcpy(at(h, 0), at(h, --h->n), h->size);
    for (size_t i = 0, c; (c = 2 * i + 1) < h->n; i = c) {
        if (c + 1 < h->n && h->cmp(at(h, c + 1), at(h, c)) > 0) c++;
        if (h->cmp(at(h, i), at(h, c)) >= 0) break;
        swap(h, i, c);
    }
}

void gheap_free(gheap *h) { free(h->a); }
