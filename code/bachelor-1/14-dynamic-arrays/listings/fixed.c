// fixed.c: the same interface on an array of fixed capacity.
#include "vec.h"
#include <stdio.h>
#include <stdlib.h>

enum { CAPACITY = 16 };

struct vec {
    int data[CAPACITY];
    size_t size;
};

vec *vec_new(void) {
    vec *v = malloc(sizeof *v);
    if (v == NULL) {
        perror("vec");
        exit(1);
    }
    v->size = 0;
    return v;
}

void vec_free(vec *v) { free(v); }
size_t vec_size(const vec *v) { return v->size; }
int vec_get(const vec *v, size_t i) { return v->data[i]; }
void vec_set(vec *v, size_t i, int x) { v->data[i] = x; }
size_t vec_capacity(const vec *v) { (void)v; return CAPACITY; }
long vec_copies(const vec *v) { (void)v; return 0; }

void vec_push(vec *v, int x) {
    if (v->size == CAPACITY) {
        fflush(stdout);
        fprintf(stderr, "vec: full at %d elements\n", CAPACITY);
        exit(1);
    }
    v->data[v->size++] = x;
}

int vec_pop(vec *v) { return v->data[--v->size]; }
