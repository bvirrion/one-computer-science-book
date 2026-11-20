// exo_lengths.c: strlen and sizeof of literals and arrays.
#include <stdio.h>
#include <string.h>

int main(void)
{
    char a[] = "rain";
    char b[20] = "rain";
    const char *c = "rain";
    char d[] = "rain\0fall";
    printf("%zu %zu\n", strlen(a), sizeof a);
    printf("%zu %zu\n", strlen(b), sizeof b);
    printf("%zu %zu\n", strlen(c), sizeof c);
    printf("%zu %zu\n", strlen(d), sizeof d);
    return 0;
}
