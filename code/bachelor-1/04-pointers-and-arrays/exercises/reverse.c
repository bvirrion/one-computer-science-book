// reverse.c: two pointers walk towards each other.
#include "reverse.h"

size_t reverse(int *a, size_t n)
{
    if (n < 2)
        return 0;
    size_t swaps = 0;
    int *left = a, *right = a + n - 1;
    while (left < right) {
        int t = *left;
        *left = *right;
        *right = t;
        left++;
        right--;
        swaps++;
    }
    return swaps;
}
