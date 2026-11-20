// swap_value.c: a swap that swaps nothing.
#include <stdio.h>

void swap(int a, int b)
{
    int t = a;
    a = b;
    b = t;
    printf("inside swap: a = %d, b = %d\n", a, b);
}

int main(void)
{
    int x = 1, y = 2;
    swap(x, y);
    printf("after swap:  x = %d, y = %d\n", x, y);
    return 0;
}
