// grid_flat.c: the same grid as one block, indexed by hand.
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t h = 3, w = 5;
    double *g = calloc(h * w, sizeof *g);               // one block of h * w doubles
    if (g == NULL)
        return 1;
    g[2 * w + 4] = 1.5;                                 // element (2, 4): index i * w + j
    printf("g[2 * w + 4] = %.1f, 1 block of %zu bytes\n", g[2 * w + 4], h * w * sizeof *g);
    free(g);
    return 0;
}
