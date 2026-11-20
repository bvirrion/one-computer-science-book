// double_free.c: two pointers to one block, each freed.
#include <stdlib.h>

int main(void)
{
    int *a = malloc(8 * sizeof *a);
    int *b = a;                                      // b and a point to the same block
    free(a);
    free(b);                                         // the same block, freed again
    return 0;
}
