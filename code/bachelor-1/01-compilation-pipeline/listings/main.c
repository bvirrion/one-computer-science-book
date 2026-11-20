// main.c: uses the square module through its header.
#include <stdio.h>
#include "square.h"

int main(void)
{
    long total = 0;
    for (long i = 1; i <= 10; i++)
        total += square(i);
    printf("sum of the first ten squares: %ld\n", total);
    printf("square was called %d times\n", square_calls);
    return 0;
}
