// radix_demo.c: LSD radix sort of six 3-digit keys, one pass per digit.
// capture: with=radix.c
#include "radix.h"
#include <stdio.h>
#include <string.h>

static void show(const char *what, const int *a, int n) {
    printf("%-16s", what);
    for (int i = 0; i < n; i++) printf(" %03d", a[i]);
    printf("\n");
}

int main(void) {
    int a[] = {329, 457, 657, 839, 436, 720, 355}, tmp[7], n = 7;
    show("input", a, n);
    const char *names[] = {"by units", "by tens", "by hundreds"};
    for (int p = 0, place = 1; p < 3; p++, place *= 10) {
        counting_sort_digit(a, tmp, n, place);
        memcpy(a, tmp, sizeof a);
        show(names[p], a, n);
    }
    return 0;
}
