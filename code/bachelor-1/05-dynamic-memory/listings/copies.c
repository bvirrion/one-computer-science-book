// copies.c: element copies made by two growth rules, counted without allocating.
#include <stdio.h>

long copies_plus_one(long n)        // capacity 1, 2, 3, ...: copy everything each time
{
    long copies = 0;
    for (long cap = 1; cap < n; cap++)
        copies += cap;              // growing from cap to cap + 1 copies cap elements
    return copies;
}

long copies_doubling(long n)        // capacity 1, 2, 4, 8, ...
{
    long copies = 0;
    for (long cap = 1; cap < n; cap *= 2)
        copies += cap;
    return copies;
}

int main(void)
{
    printf("%9s %15s %12s %7s\n", "n", "+1 copies", "x2 copies", "x2 / n");
    for (long n = 1000; n <= 1000000; n *= 10)
        printf("%9ld %15ld %12ld %7.3f\n", n, copies_plus_one(n), copies_doubling(n),
               (double)copies_doubling(n) / (double)n);
    return 0;
}
