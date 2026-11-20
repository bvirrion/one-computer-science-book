/* ex5_sum_test.c: the fixed sum equals the serial one for every p and many sizes. */
#define main ex5_main
#include "../exercises/ex5_sum.c"
#undef main
#include <assert.h>

int main(void)
{
    for (size_t n = 0; n < 2000; n += 37) {
        int *a = malloc((n + 1) * sizeof *a);
        long want = 0;
        for (size_t i = 0; i < n; i++) { a[i] = (int)(i * 7919 % 1001) - 500; want += a[i]; }
        for (int p = 1; p <= 8; p++) assert(par_sum(a, n, p) == want);
        free(a);
    }
    return 0;
}
