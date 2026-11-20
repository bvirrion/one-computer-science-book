// grid2d.h: a grid of h rows of w ints, one heap block per row (exercise 8).
#ifndef GRID2D_H
#define GRID2D_H
#include <stddef.h>

int **grid2d_new(size_t h, size_t w);    // zero-filled; NULL if out of memory (nothing leaks)
void grid2d_free(int **g, size_t h);     // frees the rows, then the table; g may be NULL

#endif
