// grid_rows.c: a grid of h x w doubles as h separate rows.
#include <stdio.h>
#include <stdlib.h>

double **grid_new(size_t h, size_t w)
{
    double **rows = malloc(h * sizeof *rows);          // h pointers
    if (rows == NULL)
        return NULL;
    for (size_t i = 0; i < h; i++) {
        rows[i] = calloc(w, sizeof *rows[i]);           // one block per row
        if (rows[i] == NULL) {
            while (i > 0)
                free(rows[--i]);                        // undo what was done
            free(rows);
            return NULL;
        }
    }
    return rows;
}

void grid_free(double **rows, size_t h)
{
    for (size_t i = 0; i < h; i++)
        free(rows[i]);                                  // the rows first,
    free(rows);                                         // then the table of rows
}

int main(void)
{
    size_t h = 3, w = 5;
    double **g = grid_new(h, w);
    if (g == NULL)
        return 1;
    g[2][4] = 1.5;                                      // two dereferences
    printf("g[2][4] = %.1f, %zu + 1 blocks\n", g[2][4], h);
    grid_free(g, h);
    return 0;
}
