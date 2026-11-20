// str_append.c: find the end of dst, copy while there is room for the zero byte.
#include "str_append.h"

int str_append(char *dst, size_t cap, const char *src)
{
    if (cap == 0)
        return -1;
    size_t n = 0;
    while (n < cap && dst[n] != '\0')
        n++;
    if (n == cap)                                       // dst was not terminated within cap
        return -1;
    while (*src != '\0' && n + 1 < cap)
        dst[n++] = *src++;
    dst[n] = '\0';
    return *src == '\0' ? 0 : -1;
}
