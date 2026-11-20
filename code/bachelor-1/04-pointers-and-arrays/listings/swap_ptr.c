// swap_ptr.c: the swap of the previous chapter, given addresses this time.
#include <stdio.h>

void swap(int *a, int *b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

int main(void)
{
    int x = 1, y = 2;
    swap(&x, &y);
    printf("after swap: x = %d, y = %d\n", x, y);
    return 0;
}
