// test-with: ../listings/sorts.c ../listings/radix.c ../exercises/inversions.c
// Every sort against qsort on random and adversarial inputs; radix sort; inversions
// against the quadratic count.
#include "radix.h"
#include "sorts.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

long inversions(const int *a, int n);

static int up(const void *x, const void *y) {
    int p = *(const int *)x, q = *(const int *)y;
    return (p > q) - (p < q);
}

int main(void) {
    void (*sorts[])(int *, int) = {insertion_sort, quicksort_basic, quicksort, quicksort3,
                                   merge_sort, merge_sort_bottom_up, heap_sort};
    static int a[3000], b[3000], c[3000];
    unsigned s = 23;
    for (int n = 0; n <= 3000; n += n < 40 ? 1 : 371) {
        for (int kind = 0; kind < 6; kind++) {
            for (int i = 0; i < n; i++) {
                s = s * 1103515245u + 12345u;
                a[i] = kind == 0 ? (int)(s >> 8) % 100000 : kind == 1 ? i : kind == 2 ? n - i
                     : kind == 3 ? 5 : kind == 4 ? (int)(s >> 8) % 3 : (i < n / 2 ? i : n - i);
            }
            memcpy(b, a, (size_t)n * sizeof *a);
            qsort(b, (size_t)n, sizeof *b, up);
            for (int k = 0; k < 7; k++) {
                if (k == 1 && n > 1000 && kind != 0 && kind != 4) continue;  // quadratic cases
                if (k == 0 && n > 1000) continue;
                memcpy(c, a, (size_t)n * sizeof *a);
                sorts[k](c, n);
                assert(memcmp(b, c, (size_t)n * sizeof *b) == 0);
            }
            memcpy(c, a, (size_t)n * sizeof *a);
            radix_sort(c, n, 6);
            assert(memcmp(b, c, (size_t)n * sizeof *b) == 0);
            if (n <= 300) {
                long q = 0;
                for (int i = 0; i < n; i++)
                    for (int j = i + 1; j < n; j++) q += a[i] > a[j];
                assert(inversions(a, n) == q);
            }
        }
    }
    puts("sorts: ok");
    return 0;
}
