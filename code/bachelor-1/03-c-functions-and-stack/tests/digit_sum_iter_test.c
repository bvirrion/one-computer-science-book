// test-with: ../exercises/digit_sum_iter.c
#include <assert.h>
#include <stdio.h>
#include "../exercises/digit_sum_iter.h"

static int digit_sum_rec(unsigned long long n)
{
    return n < 10 ? (int)n : digit_sum_rec(n / 10) + (int)(n % 10);
}

int main(void)
{
    assert(digit_sum_iter(0) == 0);
    assert(digit_sum_iter(7) == 7);
    assert(digit_sum_iter(2026) == 10);
    assert(digit_sum_iter(18446744073709551615ULL) == 87);
    for (unsigned long long n = 0; n < 200000; n += 7)
        assert(digit_sum_iter(n) == digit_sum_rec(n));
    puts("digit_sum_iter_test: ok");
    return 0;
}
