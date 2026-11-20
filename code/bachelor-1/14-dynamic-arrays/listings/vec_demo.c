// vec_demo.c: a user of the abstract type, which knows only vec.h.
// capture: with=vec.c
#include "vec.h"
#include <stdio.h>

static void show(const char *op, int x, const vec *v) {
    printf("%s %2d: size %2zu  capacity %2zu  copies so far %2ld\n", op, x,
           vec_size(v), vec_capacity(v), vec_copies(v));
}

int main(void) {
    vec *v = vec_new();
    for (int i = 1; i <= 17; i++) {
        vec_push(v, i);
        show("push", i, v);
    }
    long sum = 0;
    for (size_t i = 0; i < vec_size(v); i++) sum += vec_get(v, i);
    printf("sum of the elements: %ld\n", sum);
    while (vec_size(v) > 0) {  // print only the pops that shrink the array
        size_t before = vec_capacity(v);
        int x = vec_pop(v);
        if (vec_capacity(v) != before) show("pop ", x, v);
    }
    vec_free(v);
    return 0;
}
