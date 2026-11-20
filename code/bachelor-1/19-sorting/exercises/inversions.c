// inversions.c: the number of inversions of a[0..n), counted while merge sorting a copy.
#include <stdlib.h>
#include <string.h>

static long count(int *a, int n, int *tmp) {
    if (n < 2) return 0;
    int h = n / 2, i = 0, j = h;
    long inv = count(a, h, tmp) + count(a + h, n - h, tmp);
    for (int k = 0; k < n; k++)
        if (i < h && (j == n || a[i] <= a[j])) tmp[k] = a[i++];
        else inv += h - i, tmp[k] = a[j++];  // a[j] < the h - i keys left
    memcpy(a, tmp, (size_t)n * sizeof *a);
    return inv;
}

long inversions(const int *a, int n) {
    int *b = malloc((size_t)n * sizeof *b + 1), *tmp = malloc((size_t)n * sizeof *tmp + 1);
    if (b == NULL || tmp == NULL) exit(1);
    memcpy(b, a, (size_t)n * sizeof *a);
    long inv = count(b, n, tmp);
    free(b), free(tmp);
    return inv;
}
