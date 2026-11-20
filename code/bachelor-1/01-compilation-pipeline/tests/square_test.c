// test-with: ../listings/square.c
#include <assert.h>
#include <stdio.h>
#include "square.h"

int main(void)
{
    assert(square(0) == 0);
    assert(square(-3) == 9);
    assert(square(100000) == 10000000000L);
    assert(square_calls == 3);
    puts("square_test: ok");
    return 0;
}
