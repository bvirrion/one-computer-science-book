// rowmajor.c: a 3 x 4 array is twelve ints in a row.
#include <stdio.h>

int main(void)
{
    int g[3][4];
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 4; j++)
            g[i][j] = 10 * i + j;
    int *flat = &g[0][0];
    for (int k = 0; k < 12; k++)
        printf("%d%c", flat[k], k % 4 == 3 ? '\n' : ' ');
    printf("g[2][1] is element %td of the block\n", &g[2][1] - flat);
    printf("sizeof g = %zu, sizeof g[0] = %zu\n", sizeof g, sizeof g[0]);
    return 0;
}
