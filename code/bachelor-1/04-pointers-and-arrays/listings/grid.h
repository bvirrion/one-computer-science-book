// grid.h: a grid of h rows and w columns kept row-major in one block of ints.
#ifndef GRID_H
#define GRID_H

int *cell(int *g, int w, int i, int j);              // the address of cell (i, j)
long row_sum(const int *g, int w, int i);            // walks one row: stride 1
long col_sum(const int *g, int w, int h, int j);     // walks one column: stride w
long transpose(int *g, int n);                       // n x n, in place; returns the swaps
void print_grid(const int *g, int h, int w);

#endif
