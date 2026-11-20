// grid.c: the index map (i, j) -> i * w + j, and walks along rows and columns.
#include <stdio.h>
#include "grid.h"

int *cell(int *g, int w, int i, int j)
{
    return g + i * w + j;
}

long row_sum(const int *g, int w, int i)
{
    long s = 0;
    for (const int *p = g + i * w; p < g + (i + 1) * w; p++)
        s += *p;
    return s;
}

long col_sum(const int *g, int w, int h, int j)
{
    long s = 0;
    for (const int *p = g + j; p < g + h * w; p += w)
        s += *p;
    return s;
}

long transpose(int *g, int n)
{
    long swaps = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {            // above the diagonal only
            int t = g[i * n + j];
            g[i * n + j] = g[j * n + i];
            g[j * n + i] = t;
            swaps++;
        }
    return swaps;
}

void print_grid(const int *g, int h, int w)
{
    for (int i = 0; i < h; i++)
        for (int j = 0; j < w; j++)
            printf("%3d%s", g[i * w + j], j + 1 < w ? " " : "\n");
}
