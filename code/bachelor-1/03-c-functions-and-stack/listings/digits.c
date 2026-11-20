// digits.c: three recursive functions on numbers.
#include <stdio.h>

int digit_sum(unsigned n)               // the sum of the decimal digits of n
{
    if (n < 10)
        return (int)n;                   // base case: one digit
    return digit_sum(n / 10) + (int)(n % 10);
}

void print_binary(unsigned n)            // the binary representation of n
{
    if (n >= 2)
        print_binary(n / 2);             // the leading bits first
    putchar('0' + n % 2);
}

long power(long x, unsigned n)           // x to the n, in about log2(n) calls
{
    if (n == 0)
        return 1;
    long half = power(x, n / 2);
    return n % 2 == 0 ? half * half : half * half * x;
}

int main(void)
{
    printf("digit_sum(2026) = %d\n", digit_sum(2026));
    printf("2026 in binary  = ");
    print_binary(2026);
    printf("\npower(3, 13)    = %ld\n", power(3, 13));
    return 0;
}
