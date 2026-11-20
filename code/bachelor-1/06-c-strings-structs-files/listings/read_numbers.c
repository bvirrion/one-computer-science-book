// read_numbers.c: read one whole number per line; report bad lines on stderr and go on.
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    char line[64];
    long total = 0;
    int good = 0, lineno = 0;
    while (fgets(line, sizeof line, stdin) != NULL) {
        lineno++;
        line[strcspn(line, "\n")] = '\0';              // drop the newline, if any
        char *end;
        errno = 0;
        long v = strtol(line, &end, 10);
        if (end == line || *end != '\0' || errno == ERANGE) {
            fprintf(stderr, "line %d: not a number: \"%s\"\n", lineno, line);
            continue;
        }
        total += v;
        good++;
    }
    printf("%d numbers, total %ld\n", good, total);
    return 0;
}
