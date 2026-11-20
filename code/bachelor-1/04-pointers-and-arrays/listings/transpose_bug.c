// transpose_bug.c: a colleague's transpose, built with the address sanitizer.
// built with -O0 -g -fsanitize=address (see transpose_asan.sh)
#include <stdio.h>

void transpose(int *g, int n)
{
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j <= n; j++) {           // <= : one column too far
            int t = g[i * n + j];
            g[i * n + j] = g[j * n + i];
            g[j * n + i] = t;
        }
}

int main(void)
{
    int g[9] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    transpose(g, 3);
    for (int k = 0; k < 9; k++)
        printf("%d ", g[k]);
    printf("\n");
    return 0;
}
