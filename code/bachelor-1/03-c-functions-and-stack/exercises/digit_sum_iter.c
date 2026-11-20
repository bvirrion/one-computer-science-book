// digit_sum_iter.c: one frame, whatever the number of digits.
#include "digit_sum_iter.h"

int digit_sum_iter(unsigned long long n)
{
    int sum = 0;
    while (n >= 10) {                    // invariant: sum + digit_sum(n) is the answer
        sum += (int)(n % 10);
        n /= 10;
    }
    return sum + (int)n;
}
