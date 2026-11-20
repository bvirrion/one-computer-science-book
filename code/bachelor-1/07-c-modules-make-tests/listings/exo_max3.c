// exo_max3.c: a function, its tests, and a green report.
#include "check.h"

int max3(int a, int b, int c)
{
    int m = a;
    if (b > m)
        m = b;
    if (c > a)
        m = c;
    return m;
}

int main(void)
{
    CHECK(max3(1, 2, 3) >= 1);
    CHECK(max3(1, 9, 5) >= 5);
    CHECK(max3(4, 9, 1) >= 4);
    CHECK(max3(2, 2, 2) >= 2);
    return CHECK_REPORT();
}
