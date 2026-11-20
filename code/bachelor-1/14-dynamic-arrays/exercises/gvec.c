// gvec.c: the doubling array, with bytes instead of ints.
#include "gvec.h"
#include <stdlib.h>
#include <string.h>

struct gvec {
    unsigned char *data;
    size_t elem_size, size, capacity;
};

static void resize(gvec *v, size_t capacity) {
    unsigned char *data = malloc(capacity * v->elem_size);
    if (data == NULL) exit(1);
    if (v->size > 0) memcpy(data, v->data, v->size * v->elem_size);
    free(v->data);
    v->data = data;
    v->capacity = capacity;
}

gvec *gvec_new(size_t elem_size) {
    gvec *v = malloc(sizeof *v);
    if (v == NULL) exit(1);
    *v = (gvec){NULL, elem_size, 0, 0};
    resize(v, 1);
    return v;
}

void gvec_free(gvec *v) {
    free(v->data);
    free(v);
}

size_t gvec_size(const gvec *v) { return v->size; }
void *gvec_at(gvec *v, size_t i) { return v->data + i * v->elem_size; }

void gvec_push(gvec *v, const void *elem) {
    if (v->size == v->capacity) resize(v, 2 * v->capacity);
    memcpy(gvec_at(v, v->size++), elem, v->elem_size);
}

void gvec_pop(gvec *v, void *out) {
    memcpy(out, gvec_at(v, --v->size), v->elem_size);
    if (v->capacity > 1 && v->size <= v->capacity / 4) resize(v, v->capacity / 2);
}
