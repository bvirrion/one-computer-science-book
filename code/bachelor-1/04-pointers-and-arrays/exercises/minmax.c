// minmax.c: one pass, two results through pointers.
#include "minmax.h"

int min_max(const int *a, size_t n, int *min, int *max)
{
    if (n == 0)
        return -1;
    int lo = a[0], hi = a[0];
    for (size_t i = 1; i < n; i++) {
        if (a[i] < lo)
            lo = a[i];
        if (a[i] > hi)
            hi = a[i];
    }
    *min = lo;
    *max = hi;
    return 0;
}
