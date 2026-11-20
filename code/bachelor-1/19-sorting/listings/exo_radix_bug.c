// exo_radix_bug.c: exercise 6, a counting sort that fills each digit's block from its end.
#include <stdio.h>
#include <string.h>

void digit_sort(const int *in, int *out, int n, int place) {
    int end[10] = {0};
    for (int i = 0; i < n; i++) end[in[i] / place % 10]++;
    for (int d = 1; d < 10; d++) end[d] += end[d - 1];  // end[d]: one past the block of d
    for (int i = 0; i < n; i++) out[--end[in[i] / place % 10]] = in[i];
}

int main(void) {
    int a[] = {329, 457, 657, 839, 436, 720, 355}, tmp[7];
    for (int place = 1; place <= 100; place *= 10) {
        digit_sort(a, tmp, 7, place);
        memcpy(a, tmp, sizeof a);
    }
    for (int i = 0; i < 7; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
