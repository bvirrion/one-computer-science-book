// test-with: ../exercises/binom_count.c
#include <assert.h>
#include <stdio.h>
#include "../exercises/binom_count.h"

int main(void)
{
    long pascal[21][21] = {{0}};
    for (int n = 0; n <= 20; n++) {
        pascal[n][0] = pascal[n][n] = 1;
        for (int k = 1; k < n; k++)
            pascal[n][k] = pascal[n - 1][k - 1] + pascal[n - 1][k];
    }
    for (int n = 0; n <= 20; n++)
        for (int k = 0; k <= n; k++) {
            long calls = 0;
            assert(binom_counted(n, k, &calls) == pascal[n][k]);
            assert(calls == 2 * pascal[n][k] - 1);       // exercise 8
        }
    puts("binom_test: ok");
    return 0;
}
