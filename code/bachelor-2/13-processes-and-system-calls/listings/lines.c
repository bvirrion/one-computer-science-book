/* lines.c: print n numbered lines, through the library's buffer or without it (exercise 11). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    int n = argc > 1 ? atoi(argv[1]) : 10;
    if (argc > 2 && strcmp(argv[2], "unbuffered") == 0)
        setvbuf(stdout, NULL, _IONBF, 0);             /* every printf goes straight out */
    for (int k = 1; k <= n; k++)
        printf("line %04d\n", k);
    return 0;
}
