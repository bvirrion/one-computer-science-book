// square.c: the implementation of the square module.
#include "square.h"

int square_calls = 0;

long square(long x)
{
    square_calls++;
    return x * x;
}
