// args.c: command-line arguments, and two ways to turn them into numbers.
// capture: args=12 7x -3 hello 99999999999
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    printf("argc = %d, argv[0] = \"%s\"\n", argc, argv[0]);
    for (int i = 1; i < argc; i++) {
        char *end;
        errno = 0;
        long v = strtol(argv[i], &end, 10);
        const char *verdict = end == argv[i] ? "no digits"
                            : *end != '\0'   ? "trailing characters"
                            : errno == ERANGE ? "out of range"
                                              : "ok";
        printf("%-12s atoi = %11d   strtol = %20ld  %s\n", argv[i], atoi(argv[i]), v, verdict);
    }
    return 0;
}
