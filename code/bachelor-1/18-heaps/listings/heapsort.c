// heapsort.c: sorting in place with a max-heap; comparisons counted against 2 n lg n.
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static long compares;

static void sift_down_max(int *a, int n, int i) {
    for (int c; (c = 2 * i + 1) < n; i = c) {
        if (c + 1 < n && (compares++, a[c + 1] > a[c])) c++;  // the larger child
        if (compares++, a[i] >= a[c]) return;
        int t = a[i];
        a[i] = a[c], a[c] = t;
    }
}

void heapsort(int *a, int n) {
    for (int i = n / 2 - 1; i >= 0; i--) sift_down_max(a, n, i);  // build a max-heap
    for (int end = n - 1; end > 0; end--) {
        int t = a[0];  // the maximum goes to the end of the heap part
        a[0] = a[end], a[end] = t;
        sift_down_max(a, end, 0);  // a[end..n) is sorted and holds the largest keys
    }
}

int main(void) {
    printf("%8s %12s %8s %8s\n", "n", "comparisons", "/ n lg n", "sorted");
    unsigned s = 3;
    for (int n = 1000; n <= 1000000; n *= 10) {
        int *a = malloc((size_t)n * sizeof *a), ok = 1;
        for (int i = 0; i < n; i++) a[i] = (int)((s = s * 1103515245u + 12345u) >> 8);
        compares = 0;
        heapsort(a, n);
        for (int i = 1; i < n; i++) ok &= a[i - 1] <= a[i];
        printf("%8d %12ld %8.3f %8s\n", n, compares, compares / (n * log2(n)), ok ? "yes" : "no");
        free(a);
    }
    return 0;
}
