// vec.c: a dynamic array that doubles when full and halves when a quarter full.
#include "vec.h"
#include <stdio.h>
#include <stdlib.h>

struct vec {
    int *data;
    size_t size, capacity;
    long copies;
};
// representation invariant: 1 <= capacity, size <= capacity, data holds capacity
// cells, and size > capacity / 4 unless capacity == 1 or the array was just made

static void resize(vec *v, size_t capacity) {
    int *data = malloc(capacity * sizeof *data);
    if (data == NULL) {
        perror("vec");
        exit(1);
    }
    for (size_t i = 0; i < v->size; i++) data[i] = v->data[i];
    v->copies += (long)v->size;
    free(v->data);
    v->data = data;
    v->capacity = capacity;
}

vec *vec_new(void) {
    vec *v = malloc(sizeof *v);
    if (v == NULL) {
        perror("vec");
        exit(1);
    }
    *v = (vec){.data = NULL, .size = 0, .capacity = 0, .copies = 0};
    resize(v, 1);
    return v;
}

void vec_free(vec *v) {
    free(v->data);
    free(v);
}

size_t vec_size(const vec *v) { return v->size; }
int vec_get(const vec *v, size_t i) { return v->data[i]; }
void vec_set(vec *v, size_t i, int x) { v->data[i] = x; }
size_t vec_capacity(const vec *v) { return v->capacity; }
long vec_copies(const vec *v) { return v->copies; }

void vec_push(vec *v, int x) {
    if (v->size == v->capacity) resize(v, 2 * v->capacity);
    v->data[v->size++] = x;
}

int vec_pop(vec *v) {
    int x = v->data[--v->size];
    if (v->capacity > 1 && v->size <= v->capacity / 4) resize(v, v->capacity / 2);
    return x;
}
