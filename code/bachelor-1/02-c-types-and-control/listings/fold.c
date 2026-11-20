// fold.c: the optimiser may assume that signed overflow never happens.
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

int bigger_after_increment(int x)
{
    return x + 1 > x;
}

int main(int argc, char **argv)
{
    int x = argc > 1 ? atoi(argv[1]) : INT_MAX;
    printf("x + 1 > x for x = %d gives %d\n", x, bigger_after_increment(x));
    return 0;
}
