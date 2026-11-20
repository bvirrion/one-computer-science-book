// minmax.h: the smallest and the largest element (exercise 7).
#ifndef MINMAX_H
#define MINMAX_H
#include <stddef.h>

// Stores the minimum and the maximum of a[0..n-1] into *min and *max.
// Returns 0, or -1 (and stores nothing) when n == 0.
int min_max(const int *a, size_t n, int *min, int *max);

#endif
