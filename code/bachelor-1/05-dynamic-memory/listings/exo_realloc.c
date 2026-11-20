// exo_realloc.c: what survives a realloc?
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *a = malloc(3 * sizeof *a);
    if (a == NULL)
        return 1;
    a[0] = 7; a[1] = 8; a[2] = 9;
    int *b = realloc(a, 1000 * sizeof *a);            // likely to move to a new block
    if (b == NULL) {
        free(a);
        return 1;
    }
    b[3] = b[0] + b[2];
    printf("%d %d %d %d\n", b[0], b[1], b[2], b[3]);
    free(b);
    return 0;
}
