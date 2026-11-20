// midpoint.c: the middle of two large indices.
// capture: cflags=-O0 -fsanitize=undefined
#include <stdio.h>

int middle(int lo, int hi)
{
    return (lo + hi) / 2;
}

int main(void)
{
    printf("middle(10, 20) = %d\n", middle(10, 20));
    printf("middle(2000000000, 2100000000) = %d\n", middle(2000000000, 2100000000));
    return 0;
}
