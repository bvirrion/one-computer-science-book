// my_strdup.c: count, allocate one more byte, copy.
#include <stdlib.h>
#include "my_strdup.h"

char *my_strdup(const char *s)
{
    size_t n = 0;
    while (s[n] != '\0')
        n++;
    char *copy = malloc(n + 1);                         // + 1: the final zero byte
    if (copy == NULL)
        return NULL;
    for (size_t i = 0; i <= n; i++)                     // <= n: copies the zero too
        copy[i] = s[i];
    return copy;
}
