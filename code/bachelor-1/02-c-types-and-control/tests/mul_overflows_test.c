// test-with: ../exercises/mul_overflows.c
#include <assert.h>
#include <stdio.h>
#include "../exercises/mul_overflows.h"

static void check(int64_t a, int64_t b)
{
    int64_t r;
    assert(mul_overflows(a, b) == __builtin_mul_overflow(a, b, &r));
}

int main(void)
{
    int64_t v[] = {0, 1, -1, 2, -2, 3, 1000003, -1000003, 3037000499LL, 3037000500LL,
                   -3037000499LL, -3037000500LL, INT64_MAX, INT64_MIN, INT64_MAX / 2,
                   INT64_MIN / 2, (INT64_MIN / 2) - 1, 4294967296LL, -4294967296LL};
    int n = sizeof v / sizeof v[0];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            check(v[i], v[j]);
    puts("mul_overflows_test: ok");
    return 0;
}
