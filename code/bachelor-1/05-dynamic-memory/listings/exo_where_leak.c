// exo_where_leak.c: one path through this function leaks.
#include <stdio.h>
#include <stdlib.h>

int sum_file(const char *path, long *total)
{
    int *buffer = malloc(1000 * sizeof *buffer);
    if (buffer == NULL)
        return -1;
    FILE *f = fopen(path, "r");
    if (f == NULL)
        return -1;
    size_t n = 0;
    while (n < 1000 && fscanf(f, "%d", &buffer[n]) == 1)
        n++;
    fclose(f);
    *total = 0;
    for (size_t i = 0; i < n; i++)
        *total += buffer[i];
    free(buffer);
    return 0;
}
