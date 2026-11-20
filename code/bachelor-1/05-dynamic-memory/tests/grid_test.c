// test-with: ../exercises/grid2d.c
#include <assert.h>
#include <stdio.h>
#include "../exercises/grid2d.h"

int main(void)
{
    int **g = grid2d_new(4, 7);
    assert(g != NULL);
    for (size_t i = 0; i < 4; i++)
        for (size_t j = 0; j < 7; j++) {
            assert(g[i][j] == 0);
            g[i][j] = (int)(10 * i + j);
        }
    assert(g[3][6] == 36);
    grid2d_free(g, 4);
    grid2d_free(NULL, 0);
    puts("grid_test: ok");
    return 0;
}
