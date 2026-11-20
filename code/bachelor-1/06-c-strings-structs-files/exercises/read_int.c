// read_int.c: strtol, then check everything it reports.
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include "read_int.h"

int read_int(const char *s, int *out)
{
    char *end;
    errno = 0;
    long v = strtol(s, &end, 10);
    if (end == s)                                       // no digits at all (empty, or not a number)
        return -1;
    if (errno == ERANGE || v < INT_MIN || v > INT_MAX)  // too large for long, or for int
        return -1;
    while (isspace((unsigned char)*end))                // trailing spaces and the newline are fine
        end++;
    if (*end != '\0')
        return -1;
    *out = (int)v;
    return 0;
}
