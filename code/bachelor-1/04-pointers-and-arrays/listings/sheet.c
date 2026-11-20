// sheet.c: a 4 x 4 sheet in a flat array: sums, a transpose, and its count of swaps.
// capture: with=grid.c
#include <stdio.h>
#include "grid.h"

int main(void)
{
    int g[16];
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            *cell(g, 4, i, j) = 10 * i + j;
    print_grid(g, 4, 4);
    printf("row 2 sums to %ld, column 3 to %ld\n", row_sum(g, 4, 2), col_sum(g, 4, 4, 3));
    long swaps = transpose(g, 4);
    printf("after the transpose (%ld swaps):\n", swaps);
    print_grid(g, 4, 4);
    for (int n = 1; n <= 8; n++) {
        int big[64] = {0};
        printf("n = %d: %ld swaps\n", n, transpose(big, n));
    }
    return 0;
}
