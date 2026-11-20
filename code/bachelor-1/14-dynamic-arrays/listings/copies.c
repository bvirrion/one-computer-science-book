// copies.c: element copies made by n pushes, for three growth policies.
#include <stdio.h>

// the capacity after growing a full array of capacity c
static long grow(int policy, long c) {
    if (policy == 0) return c + c / 2 + 1;  // factor 1.5
    if (policy == 1) return 2 * c;          // factor 2
    return c + 16;                          // 16 more cells
}

static long copies(int policy, long n) {
    long size = 0, capacity = 1, total = 0;
    for (long i = 0; i < n; i++) {
        if (size == capacity) {
            total += size;  // a resize copies every element
            capacity = grow(policy, capacity);
        }
        size++;
    }
    return total;
}

int main(void) {
    printf("%9s %22s %22s %22s\n", "n", "x1.5: copies, per push", "x2: copies, per push",
           "+16: copies, per push");
    for (long n = 1000; n <= 1000000; n *= 10) {
        printf("%9ld", n);
        for (int policy = 0; policy < 3; policy++) {
            long c = copies(policy, n);
            printf(" %14ld %7.2f", c, (double)c / n);
        }
        printf("\n");
    }
    return 0;
}
