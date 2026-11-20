// exo_compare.c: four comparisons of mixed types.
#include <stdio.h>

int main(void)
{
    unsigned char big = 200;
    signed char neg = -1;
    unsigned u = 0;
    long l = -1;
    printf("%d %d %d %d\n", -1 < (int)u, l < 1u, big < neg, (unsigned)neg > 1000u);
    return 0;
}
