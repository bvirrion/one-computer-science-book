// exo_scanf.c: reading a number, the wrong way.
#include <stdio.h>

int main(void)
{
    int n = 0;
    if (scanf("%d", n) == 1)
        printf("read %d\n", n);
    return 0;
}
