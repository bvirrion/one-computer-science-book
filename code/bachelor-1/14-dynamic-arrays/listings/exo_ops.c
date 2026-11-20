// exo_ops.c: exercise 1.
// capture: with=vec.c
#include "vec.h"
#include <stdio.h>

int main(void) {
    vec *v = vec_new();
    for (int i = 0; i < 6; i++) vec_push(v, i);
    printf("%zu %zu\n", vec_size(v), vec_capacity(v));
    for (int i = 0; i < 4; i++) vec_pop(v);
    printf("%zu %zu\n", vec_size(v), vec_capacity(v));
    vec_push(v, 9);
    vec_push(v, 9);
    vec_push(v, 9);
    printf("%zu %zu %ld\n", vec_size(v), vec_capacity(v), vec_copies(v));
    vec_free(v);
    return 0;
}
