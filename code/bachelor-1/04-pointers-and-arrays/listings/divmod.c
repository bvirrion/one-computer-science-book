// divmod.c: two results through two pointer parameters.
#include <stdio.h>

void divmod(int a, int b, int *quotient, int *remainder)
{
    *quotient = a / b;
    *remainder = a % b;
}

int main(void)
{
    int q, r;
    divmod(2026, 7, &q, &r);
    printf("2026 = 7 * %d + %d\n", q, r);
    return 0;
}
