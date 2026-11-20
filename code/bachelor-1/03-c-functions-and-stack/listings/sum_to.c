// sum_to.c: 1 + 2 + ... + n by a tail call, for n = ten million.
#include <stdio.h>

long sum_to(long n, long acc)
{
    if (n == 0)
        return acc;
    return sum_to(n - 1, acc + n);       // the call is the last thing done
}

int main(void)
{
    printf("sum = %ld\n", sum_to(10000000, 0));
    return 0;
}
