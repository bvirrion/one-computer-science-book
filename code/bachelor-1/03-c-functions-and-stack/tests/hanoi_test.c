// test-with: ../exercises/hanoi.c
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "../exercises/hanoi.h"

int main(void)
{
    char out[64] = "";
    int depth = 0;
    assert(hanoi(2, 'A', 'C', 'B', out, 1, &depth) == 3);
    assert(strcmp(out, "A->B A->C B->C ") == 0);
    assert(depth == 3);
    for (int n = 0; n <= 20; n++) {
        depth = 0;
        assert(hanoi(n, 'A', 'C', 'B', NULL, 1, &depth) == (1L << n) - 1);
        assert(depth == n + 1);
    }
    puts("hanoi_test: ok");
    return 0;
}
