// counter.c: a binary counter of K bits, counting the bits each operation flips.
#include <stdio.h>

enum { K = 20 };

static int increment(int bits[K]) {  // returns the number of bits flipped
    int i = 0;
    while (i < K && bits[i] == 1) bits[i++] = 0;  // the trailing 1s become 0
    if (i < K) bits[i] = 1;                         // and the next 0 becomes 1
    return i < K ? i + 1 : i;
}

static int decrement(int bits[K]) {
    int i = 0;
    while (i < K && bits[i] == 0) bits[i++] = 1;  // the trailing 0s become 1
    if (i < K) bits[i] = 0;
    return i < K ? i + 1 : i;
}

int main(void) {
    printf("%7s %12s %10s\n", "n", "flips", "per incr.");
    for (long n = 8; n <= 1 << 16; n *= 8) {
        int bits[K] = {0};
        long flips = 0;
        for (long i = 0; i < n; i++) flips += increment(bits);
        printf("%7ld %12ld %10.4f\n", n, flips, (double)flips / n);
    }
    int bits[K] = {0};
    for (long i = 0; i < (1 << 15) - 1; i++) increment(bits);  // 0111...1
    long flips = 0, n = 1000;
    for (long i = 0; i < n; i++) flips += i % 2 == 0 ? increment(bits) : decrement(bits);
    printf("from 2^15 - 1, %ld increments and decrements alternating: %ld flips, %.1f each\n",
           n, flips, (double)flips / n);
    return 0;
}
