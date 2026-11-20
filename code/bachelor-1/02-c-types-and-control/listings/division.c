// division.c: integer division truncates toward zero, and % follows it.
#include <stdio.h>

int main(void)
{
    int a[] = {7, -7, 7, -7};
    int b[] = {2, 2, -2, -2};
    for (int k = 0; k < 4; k++)
        printf("%2d / %2d = %2d   %2d %% %2d = %2d\n", a[k], b[k], a[k] / b[k], a[k], b[k],
               a[k] % b[k]);
    return 0;
}
