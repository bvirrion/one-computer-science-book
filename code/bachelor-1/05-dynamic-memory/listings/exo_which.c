// exo_which.c: four functions, four memory errors.
#include <stdlib.h>
#include <string.h>

int a(void)
{
    int *p = malloc(10 * sizeof *p);
    p[10] = 1;
    free(p);
    return 0;
}

int b(int n)
{
    int *p = malloc(10 * sizeof *p);
    if (n > 100)
        return -1;
    free(p);
    return 0;
}

int c(void)
{
    char *s = malloc(6);
    strcpy(s, "hello");
    free(s);
    return s[0] == 'h';
}

int d(void)
{
    int x = 5;
    int *p = &x;
    free(p);
    return 0;
}
