// test-with: ../exercises/minmax.c
#include <assert.h>
#include <stdio.h>
#include "../exercises/minmax.h"

int main(void)
{
    int a[] = {4, -2, 9, 9, 0, -7, 3};
    int lo = 1, hi = 1;
    assert(min_max(a, 7, &lo, &hi) == 0 && lo == -7 && hi == 9);
    assert(min_max(a, 1, &lo, &hi) == 0 && lo == 4 && hi == 4);
    lo = hi = 123;
    assert(min_max(a, 0, &lo, &hi) == -1 && lo == 123 && hi == 123);
    int same[3] = {5, 5, 5};
    assert(min_max(same, 3, &lo, &hi) == 0 && lo == 5 && hi == 5);
    puts("minmax_test: ok");
    return 0;
}
