// generic_max.h: the largest element of an array of any type (exercise 11).
#ifndef GENERIC_MAX_H
#define GENERIC_MAX_H
#include <stddef.h>

// Returns the address of a largest element of the n elements of `size` bytes
// starting at base, according to cmp (same contract as for qsort); NULL if n == 0.
const void *generic_max(const void *base, size_t n, size_t size,
                        int (*cmp)(const void *, const void *));

#endif
