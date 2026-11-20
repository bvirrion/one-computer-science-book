// exo_sift_bug.c: exercise 5, a sift-down that only looks at the left child.
#include <stdio.h>

void sift_down(int *a, int n, int i) {
    for (int c; (c = 2 * i + 1) < n && a[c] < a[i]; i = c) {
        int t = a[i];
        a[i] = a[c], a[c] = t;
    }
}

int main(void) {
    int a[] = {1, 5, 2, 6, 7, 3, 4};  // a min-heap
    int n = 7, out[7];
    for (int k = 0; k < 7; k++) {  // extract the minimum seven times
        out[k] = a[0];
        a[0] = a[--n];
        sift_down(a, n, 0);
    }
    for (int k = 0; k < 7; k++) printf(k ? " %d" : "%d", out[k]);
    printf("\n");
    return 0;
}
