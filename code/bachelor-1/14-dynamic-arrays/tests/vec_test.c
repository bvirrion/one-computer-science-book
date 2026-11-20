// test-with: ../listings/vec.c
// The suite on the doubling array, then its capacity and copy counts.
#include "vec_suite.h"

int main(void) {
    vec_suite(1000);
    vec *v = vec_new();
    long ops = 0;
    unsigned state = 12345;
    for (int round = 0; round < 200000; round++) {  // random pushes and pops
        state = state * 1103515245u + 12345u;
        if (vec_size(v) == 0 || (state >> 16) % 3 != 0) vec_push(v, round);
        else vec_pop(v);
        ops++;
        size_t s = vec_size(v), c = vec_capacity(v);
        assert(s <= c && (c == 1 || s > c / 4));  // the representation invariant
        assert(vec_copies(v) <= 2 * ops);           // the elastic array theorem
    }
    vec_free(v);
    puts("vec: ok");
    return 0;
}
