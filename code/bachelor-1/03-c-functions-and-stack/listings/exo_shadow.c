// exo_shadow.c: which x is printed?
#include <stdio.h>

int x = 10;

int f(int x)
{
    x = x + 1;
    {
        int x = 100;
        x++;
    }
    return x;
}

int main(void)
{
    int y = f(x);
    printf("%d %d\n", x, y);
    for (int x = 0; x < 2; x++)
        printf("%d ", x);
    printf("%d\n", x);
    return 0;
}
