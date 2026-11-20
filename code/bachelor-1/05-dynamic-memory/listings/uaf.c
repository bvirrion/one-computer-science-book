// uaf.c: reading a block after giving it back.
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *scores = malloc(4 * sizeof *scores);
    if (scores == NULL)
        return 1;
    scores[0] = 17;
    free(scores);
    printf("first score: %d\n", scores[0]);         // scores is now a dangling pointer
    return 0;
}
