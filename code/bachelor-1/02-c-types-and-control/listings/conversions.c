// conversions.c: mixed signed and unsigned operands, and truncation.
#include <stdio.h>

int main(void)
{
    int minus_one = -1;
    unsigned one = 1;
    if (minus_one < one)
        puts("-1 < 1u is true");
    else
        puts("-1 < 1u is false");
    long big = -1;
    printf("-1L < 1u gives %d\n", big < one);
    unsigned char c = 300;               // 300 mod 256
    int i = 3.99;                        // the fraction is dropped
    int j = -3.99;
    printf("unsigned char 300 holds %d, (int)3.99 = %d, (int)-3.99 = %d\n", c, i, j);
    return 0;
}
