// exo_reset.c: two functions that try to reset a variable.
#include <stdio.h>

void reset(int x)
{
    x = 0;
}

int reset_and_return(int x)
{
    x = 0;
    return x;
}

int main(void)
{
    int a = 5, b = 5;
    reset(a);
    b = reset_and_return(b);
    printf("a = %d, b = %d\n", a, b);
    return 0;
}
