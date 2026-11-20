// exo_realloc_bad.c: growing an array, the tempting way.
#include <stdlib.h>

int grow(int **a, size_t *cap)
{
    *a = realloc(*a, 2 * *cap * sizeof **a);
    if (*a == NULL)
        return -1;
    *cap *= 2;
    return 0;
}
