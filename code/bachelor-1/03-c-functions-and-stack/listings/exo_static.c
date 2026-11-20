// exo_static.c: a running total kept between calls.
#include <stdio.h>

int add(int amount)
{
    static int total = 100;
    int before = total;
    total += amount;
    return before;
}

int main(void)
{
    int a = add(5);
    int b = add(10);
    int c = add(-20);
    printf("%d %d %d\n", a, b, c);
    return 0;
}
