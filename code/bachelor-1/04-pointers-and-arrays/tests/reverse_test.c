// test-with: ../exercises/reverse.c
#include <assert.h>
#include <stdio.h>
#include "../exercises/reverse.h"

int main(void)
{
    for (size_t n = 0; n <= 9; n++) {
        int a[9];
        for (size_t i = 0; i < n; i++)
            a[i] = (int)i;
        assert(reverse(a, n) == n / 2);              // exercise 10: floor(n/2) swaps
        for (size_t i = 0; i < n; i++)
            assert(a[i] == (int)(n - 1 - i));
    }
    puts("reverse_test: ok");
    return 0;
}
