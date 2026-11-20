/* int_vec.c: a growable array of int in C; a second one for double means a second file. */
#include <stdio.h>
#include <stdlib.h>

struct int_vec { int *data; size_t size, cap; };

int int_vec_push(struct int_vec *v, int x)
{
    if (v->size == v->cap) {
        size_t cap = v->cap ? 2 * v->cap : 1;
        int *p = realloc(v->data, cap * sizeof *p);
        if (!p)
            return -1;
        v->data = p;
        v->cap = cap;
    }
    v->data[v->size++] = x;
    return 0;
}

/* The same with void *: one copy of the code, but the types are gone. */
struct any_vec { void *data; size_t size, cap, elem; };

int any_vec_push(struct any_vec *v, const void *x)
{
    if (v->size == v->cap) {
        size_t cap = v->cap ? 2 * v->cap : 1;
        void *p = realloc(v->data, cap * v->elem);
        if (!p)
            return -1;
        v->data = p;
        v->cap = cap;
    }
    char *slot = (char *)v->data + v->size++ * v->elem;
    for (size_t i = 0; i < v->elem; i++)
        slot[i] = ((const char *)x)[i];
    return 0;
}

int main(void)
{
    struct int_vec a = {0};
    struct any_vec b = {0, 0, 0, sizeof(double)};
    for (int i = 1; i <= 5; i++) {
        int_vec_push(&a, i * i);
        double x = i / 4.0;
        any_vec_push(&b, &x);
    }
    /* any_vec_push(&b, &some_int) would compile as well: nothing checks the type */
    printf("ints: %d ... %d, doubles: %g ... %g\n", a.data[0], a.data[4], ((double *)b.data)[0],
           ((double *)b.data)[4]);
    free(a.data);
    free(b.data);
    return 0;
}
