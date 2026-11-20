// warnings_fixed.c: the same program with every warning resolved.
#include <stdio.h>

int main(void)
{
    int count = 0;
    long big = 3000000000L;
    int x = 5;

    if (x == 0)
        printf("x is zero\n");
    printf("big is %ld\n", big);
    for (int i = 0; i < 3; i++)
        count++;
    printf("count is %d\n", count);
    return 0;
}
