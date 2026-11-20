// exo_equal.c: exercise 5, quicksort on n equal keys.
// capture: with=sorts.c
#include "sorts.h"
#include <stdio.h>

int main(void) {
    static int a[4000];
    for (int n = 1000; n <= 4000; n *= 2) {
        for (int i = 0; i < n; i++) a[i] = 7;
        sort_compares = 0;
        quicksort_basic(a, n);
        long basic = sort_compares;
        sort_compares = 0;
        quicksort3(a, n);
        printf("n = %d: basic %ld comparisons, three-way %ld\n", n, basic, sort_compares);
    }
    return 0;
}
