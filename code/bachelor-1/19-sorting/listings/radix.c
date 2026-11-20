// radix.c: counting sort is stable, so each pass keeps the order of the previous ones.
#include "radix.h"
#include <stdlib.h>
#include <string.h>

void counting_sort_digit(const int *in, int *out, int n, int place) {
    int count[10] = {0};
    for (int i = 0; i < n; i++) count[in[i] / place % 10]++;
    int start[10];  // start[d]: the first output cell of the keys with digit d
    for (int d = 0, sum = 0; d < 10; d++) start[d] = sum, sum += count[d];
    for (int i = 0; i < n; i++) out[start[in[i] / place % 10]++] = in[i];  // in input order
}

void radix_sort(int *a, int n, int digits) {
    int *tmp = malloc((size_t)n * sizeof *tmp + 1);
    if (tmp == NULL) exit(1);
    for (int place = 1, p = 0; p < digits; p++, place *= 10) {  // least significant first
        counting_sort_digit(a, tmp, n, place);
        memcpy(a, tmp, (size_t)n * sizeof *a);
    }
    free(tmp);
}
