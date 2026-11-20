// mul_overflows.c: decide whether a * b overflows, without multiplying first.
#include "mul_overflows.h"

bool mul_overflows(int64_t a, int64_t b)
{
    if (a == 0 || b == 0)
        return false;
    if (a > 0) {
        if (b > 0)
            return a > INT64_MAX / b;    // both positive
        return b < INT64_MIN / a;        // a > 0, b < 0
    }
    if (b > 0)
        return a < INT64_MIN / b;        // a < 0, b > 0
    return a < INT64_MAX / b;            // both negative: a * b > 0
}
