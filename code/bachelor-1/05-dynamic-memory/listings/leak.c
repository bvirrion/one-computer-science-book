// leak.c: a pointer overwritten before its block was freed.
#include <stdio.h>
#include <stdlib.h>

char *make_label(int n)
{
    char *label = malloc(16);
    if (label != NULL)
        snprintf(label, 16, "item %d", n);
    return label;                                    // the caller must free it
}

int main(void)
{
    char *s = NULL;
    for (int i = 1; i <= 3; i++) {
        s = make_label(i);                           // the previous block's only address is lost
        printf("%s\n", s);
    }
    free(s);                                         // frees the last block only
    fflush(stdout);                                  // print now: the leak report ends the run
    return 0;
}
