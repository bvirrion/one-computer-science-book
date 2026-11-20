// classify.c: the kind of a triangle with integer sides.
#include "classify.h"

int classify(int a, int b, int c)
{
    if (a <= 0 || b <= 0 || c <= 0)
        return NOT_A_TRIANGLE;
    if (a + b <= c || a + c <= b || b + c <= a)
        return NOT_A_TRIANGLE;
    if (a == b && b == c)
        return EQUILATERAL;
    if (a == b || b == c || a == c)
        return ISOSCELES;
    return SCALENE;
}
