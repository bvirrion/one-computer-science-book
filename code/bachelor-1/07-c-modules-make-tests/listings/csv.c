// csv.c: one pass over the line.
#include <string.h>
#include "csv.h"

int csv_split(char *line, char **fields, int max)
{
    line[strcspn(line, "\r\n")] = '\0';
    int n = 0;
    char *p = line;
    for (;;) {
        if (n == max)
            return -1;
        fields[n++] = p;
        char *comma = strchr(p, ',');
        if (comma == NULL)
            return n;
        *comma = '\0';
        p = comma + 1;
    }
}
