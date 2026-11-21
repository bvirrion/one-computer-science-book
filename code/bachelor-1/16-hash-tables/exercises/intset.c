// intset.c: a set of non-negative ints by linear probing, doubling at load 3/4.
#include <stdbool.h>
#include <stdlib.h>

typedef struct {
    long *slot;  // -1: free
    size_t m, n;
} intset;

static size_t home(long x, size_t m) {  // multiply by a large odd constant, then reduce
    return (size_t)((unsigned long)x * 11400714819323198485u % m);
}

bool intset_init(intset *s) {  // false when out of memory
    s->m = 8, s->n = 0;
    s->slot = malloc(s->m * sizeof *s->slot);
    if (s->slot == NULL) return false;
    for (size_t i = 0; i < s->m; i++) s->slot[i] = -1;
    return true;
}

bool intset_has(const intset *s, long x) {
    for (size_t i = home(x, s->m); s->slot[i] != -1; i = (i + 1) % s->m)
        if (s->slot[i] == x) return true;
    return false;
}

static void place(long *slot, size_t m, long x) {
    size_t i = home(x, m);
    while (slot[i] != -1) i = (i + 1) % m;
    slot[i] = x;
}

bool intset_add(intset *s, long x) {  // precondition: x >= 0; false when out of memory
    if (intset_has(s, x)) return true;
    if (4 * (s->n + 1) > 3 * s->m) {  // rehash into twice as many slots
        long *bigger = malloc(2 * s->m * sizeof *bigger);
        if (bigger == NULL) return false;  // the set is left as it was
        for (size_t i = 0; i < 2 * s->m; i++) bigger[i] = -1;
        for (size_t i = 0; i < s->m; i++)
            if (s->slot[i] != -1) place(bigger, 2 * s->m, s->slot[i]);
        free(s->slot);
        s->slot = bigger, s->m *= 2;
    }
    place(s->slot, s->m, x);
    s->n++;
    return true;
}

void intset_free(intset *s) { free(s->slot); }
