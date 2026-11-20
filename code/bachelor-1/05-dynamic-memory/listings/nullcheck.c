// nullcheck.c: malloc says no.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t huge = SIZE_MAX / 2;                      // about 9.2e18 bytes
    char *p = malloc(huge);
    if (p == NULL)
        printf("malloc(%zu) returned NULL\n", huge);
    else
        free(p);
    return 0;
}
