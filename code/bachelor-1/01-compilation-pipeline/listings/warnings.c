// warnings.c: three bugs that the compiler reports as warnings.
#include <stdio.h>

int main(void)
{
    int count;              // never given a value
    long big = 3000000000L;
    int x = 5;

    if (x = 0)              // assignment, not a comparison
        printf("x is zero\n");
    printf("big is %d\n", big);   // %d expects an int, not a long
    for (int i = 0; i < 3; i++)
        count++;
    printf("count is %d\n", count);
    return 0;
}
