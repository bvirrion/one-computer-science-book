// generic_max.c: no types, only addresses, sizes and a comparator.
#include "generic_max.h"

const void *generic_max(const void *base, size_t n, size_t size,
                        int (*cmp)(const void *, const void *))
{
    if (n == 0)
        return NULL;
    const char *bytes = base;            // char: pointer arithmetic counts bytes
    const char *best = bytes;
    for (size_t i = 1; i < n; i++) {
        const char *element = bytes + i * size;
        if (cmp(element, best) > 0)
            best = element;
    }
    return best;
}
