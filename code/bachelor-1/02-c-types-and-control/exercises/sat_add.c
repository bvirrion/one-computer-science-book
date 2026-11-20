// sat_add.c: a + b, clamped to [INT32_MIN, INT32_MAX], with no overflow on the way.
#include "sat_add.h"

int32_t sat_add(int32_t a, int32_t b)
{
    if (b > 0 && a > INT32_MAX - b)
        return INT32_MAX;
    if (b < 0 && a < INT32_MIN - b)
        return INT32_MIN;
    return a + b;
}
