// elastic.c: the worst sequences of m pushes and pops for the policy of vec.c
// (double when full, halve when a quarter full), found by trying all 2^m of them.
#include <stdio.h>

static long copies_of(long m, long mask) {  // bit i of mask: 1 push, 0 pop
    long size = 0, capacity = 1, copies = 0;
    for (long i = 0; i < m; i++) {
        if (mask >> i & 1) {
            if (size == capacity) {
                copies += size;
                capacity *= 2;
            }
            size++;
        } else {
            if (size == 0) return -1;  // a pop on the empty array: not allowed
            size--;
            if (capacity > 1 && size <= capacity / 4) {
                copies += size;
                capacity /= 2;
            }
        }
    }
    return copies;
}

int main(void) {
    printf("%2s %6s %9s  %s\n", "m", "copies", "copies/m", "a worst sequence (+ push, - pop)");
    for (long m = 2; m <= 26; m += 2) {
        long best = -1, best_mask = 0;
        for (long mask = 0; mask < 1L << m; mask++) {
            long c = copies_of(m, mask);
            if (c > best) best = c, best_mask = mask;
        }
        printf("%2ld %6ld %9.3f  ", m, best, (double)best / m);
        for (long i = 0; i < m; i++) putchar(best_mask >> i & 1 ? '+' : '-');
        printf("\n");
    }
    return 0;
}
