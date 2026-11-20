// test-with: ../exercises/stats.c
#include <assert.h>
#include <stdio.h>
#include "../exercises/stats.h"

int main(void)
{
    double x[] = {2.0, 9.5, -1.0, 4.5};
    assert(mean(x, 4) == 3.75);
    assert(maximum(x, 4) == 9.5);
    assert(mean(x, 0) == 0.0);
    puts("stats_test: ok");
    return 0;
}
