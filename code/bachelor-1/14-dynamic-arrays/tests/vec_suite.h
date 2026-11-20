// vec_suite.h: one test suite for any implementation of vec.h, up to max_size elements.
#include "vec.h"
#include <assert.h>
#include <stdio.h>

static void vec_suite(int max_size) {
    vec *v = vec_new();
    assert(vec_size(v) == 0);
    for (int i = 0; i < max_size; i++) {
        vec_push(v, 3 * i);
        assert(vec_size(v) == (size_t)i + 1 && vec_get(v, (size_t)i) == 3 * i);
        assert(vec_capacity(v) >= vec_size(v));
    }
    for (int i = 0; i < max_size; i++) vec_set(v, (size_t)i, vec_get(v, (size_t)i) + 1);
    for (int i = max_size - 1; i >= 0; i--) assert(vec_pop(v) == 3 * i + 1);
    assert(vec_size(v) == 0);
    vec_free(v);
}
