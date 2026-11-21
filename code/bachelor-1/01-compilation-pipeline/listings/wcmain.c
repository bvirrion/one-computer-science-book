// wcmain.c: reads standard input and reports the counts.
#include <stdio.h>
#include <stdlib.h>
#include "count.h"

int main(void)
{
    char *title = malloc(16);
    if (title == NULL)
        return 1;  // no memory: stop before writing through NULL
    int c;
    snprintf(title, 16, "standard input");
    while ((c = getchar()) != EOF)
        feed(c);
    report(title);
    free(title);
    return 0;
}
