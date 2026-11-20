// exo_ptrs.c: follow the pointers.
#include <stdio.h>

int main(void)
{
    int a = 1, b = 2;
    int *p = &a, *q = &b;
    *p = *q + 10;
    p = q;
    *p = *p * 3;
    q = &a;
    *q = *q - *p;
    printf("a = %d, b = %d, *p = %d, *q = %d\n", a, b, *p, *q);
    return 0;
}
