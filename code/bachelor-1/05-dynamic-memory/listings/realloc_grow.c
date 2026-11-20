// realloc_grow.c: growing a block, keeping the old one if realloc fails.
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t cap = 4;
    int *a = malloc(cap * sizeof *a);
    if (a == NULL)
        return 1;
    for (size_t i = 0; i < cap; i++)
        a[i] = (int)(10 * i);
    int *bigger = realloc(a, 2 * cap * sizeof *a);   // a new variable: a survives a failure
    if (bigger == NULL) {
        free(a);
        return 1;
    }
    a = bigger;                                      // the old a may be invalid now: forget it
    for (size_t i = cap; i < 2 * cap; i++)
        a[i] = (int)(10 * i);
    cap *= 2;
    for (size_t i = 0; i < cap; i++)
        printf("%d ", a[i]);
    printf("\n");
    free(a);
    return 0;
}
