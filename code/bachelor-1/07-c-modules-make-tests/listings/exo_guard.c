// exo_guard.c: a program that needs points and segments.
#include "point.h"
#include "segment.h"

int main(void)
{
    struct segment s = {{0, 0}, {3, 4}};
    struct point p = s.b;
    return (int)p.x;
}
