// use_after_free.c: a street name freed, then printed.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);
    char *name = malloc(16);
    strcpy(name, "Mill Lane");
    char *shown = name;                    /* a second pointer to the same block */
    free(name);                            /* the owner gives the block back */
    printf("%s\n", shown);                 /* ...and the other pointer still uses it */
    return 0;
}
