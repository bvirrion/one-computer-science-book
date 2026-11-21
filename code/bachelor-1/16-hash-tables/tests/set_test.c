// test-with: ../exercises/intset.c
// The integer set by open addressing against a boolean array.
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { long *slot; size_t m, n; } intset;
bool intset_init(intset *s);
bool intset_has(const intset *s, long x);
bool intset_add(intset *s, long x);
void intset_free(intset *s);

int main(void) {
    intset s;
    assert(intset_init(&s));
    static bool model[100000];
    srand(4);
    for (int i = 0; i < 50000; i++) {
        long x = rand() % 100000;
        assert(intset_add(&s, x));
        model[x] = true;
        assert(4 * s.n <= 3 * s.m);
    }
    for (long x = 0; x < 100000; x++) assert(intset_has(&s, x) == model[x]);
    intset_free(&s);
    puts("set: ok");
    return 0;
}
