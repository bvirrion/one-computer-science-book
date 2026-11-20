// grid2d.c: allocate row by row; on failure, free what was allocated.
#include <stdlib.h>
#include "grid2d.h"

int **grid2d_new(size_t h, size_t w)
{
    int **g = malloc(h * sizeof *g);
    if (g == NULL)
        return NULL;
    for (size_t i = 0; i < h; i++) {
        g[i] = calloc(w, sizeof *g[i]);
        if (g[i] == NULL) {
            grid2d_free(g, i);          // the i rows made so far
            return NULL;
        }
    }
    return g;
}

void grid2d_free(int **g, size_t h)
{
    if (g == NULL)
        return;
    for (size_t i = 0; i < h; i++)
        free(g[i]);
    free(g);
}
