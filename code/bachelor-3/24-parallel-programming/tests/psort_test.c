/* psort_test.c: the threaded merge sort sorts every size, with every thread count. */
#define main psort_main
#include "../listings/psort.c"
#undef main
#include <assert.h>

static int cmp(const void *x, const void *y)
{
    int a = *(const int *)x, b = *(const int *)y;
    return (a > b) - (a < b);
}

int main(void)
{
    unsigned x = 7;
    for (size_t n = 0; n < 3000; n += 101) {
        int *src = malloc((n + 1) * sizeof *src), *a = malloc((n + 1) * sizeof *a),
            *tmp = malloc((n + 1) * sizeof *a), *want = malloc((n + 1) * sizeof *a);
        for (size_t i = 0; i < n; i++) { x = x * 1103515245u + 12345u; src[i] = (int)(x % 50); }
        memcpy(want, src, n * sizeof *a);
        qsort(want, n, sizeof *want, cmp);
        for (int p = 1; p <= 8; p++) {
            memcpy(a, src, n * sizeof *a);
            job all = {a, tmp, n, p};
            sort(&all);
            assert(memcmp(a, want, n * sizeof *a) == 0);
        }
        free(src); free(a); free(tmp); free(want);
    }
    return 0;
}
