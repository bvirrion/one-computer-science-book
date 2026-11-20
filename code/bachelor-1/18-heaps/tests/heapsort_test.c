// test-with:
// Heapsort on many sizes and inputs, and its comparison bound 2 n lg n.
#define main heapsort_main
#include "heapsort.c"
#undef main
#include <assert.h>

int main(void) {
    unsigned s = 5;
    for (int n = 1; n <= 2000; n += n < 50 ? 1 : 97) {
        int *a = malloc((size_t)n * sizeof *a);
        for (int kind = 0; kind < 4; kind++) {
            for (int i = 0; i < n; i++)
                a[i] = kind == 0 ? i : kind == 1 ? n - i : kind == 2 ? 7 : (int)((s = s * 1103515245u + 12345u) >> 20);
            compares = 0;
            heapsort(a, n);
            for (int i = 1; i < n; i++) assert(a[i - 1] <= a[i]);
            assert(n < 2 || compares <= 2 * n * log2(n));
        }
        free(a);
    }
    puts("heapsort: ok");
    return 0;
}
