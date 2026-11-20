// radix_loans.c: the returned loans sorted by date of return, written as the number yyyymmdd,
// in eight passes of counting sort; the result is checked against qsort.
// capture: with=radix.c
#include "radix.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int up(const void *x, const void *y) {
    int a = *(const int *)x, b = *(const int *)y;
    return (a > b) - (a < b);
}

int main(void) {
    static int a[400], b[400];
    FILE *f = fopen("../../../../data/town/loans.csv", "r");
    char line[128];
    int n = 0, id, book, member, y, m, d;
    if (f == NULL || fgets(line, sizeof line, f) == NULL) return 1;
    while (n < 400 && fgets(line, sizeof line, f) != NULL)
        if (sscanf(line, "%d,%d,%d,%*d-%*d-%*d,%*d-%*d-%*d,%d-%d-%d", &id, &book, &member, &y, &m,
                   &d) == 6)
            a[n++] = y * 10000 + m * 100 + d;
    fclose(f);
    memcpy(b, a, sizeof a);
    radix_sort(a, n, 8);
    qsort(b, (size_t)n, sizeof b[0], up);
    printf("%d returns; first %d, %d, %d; last %d; same as qsort: %s\n", n, a[0], a[1], a[2],
           a[n - 1], memcmp(a, b, sizeof a) == 0 ? "yes" : "no");
    return 0;
}
