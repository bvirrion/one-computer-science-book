// precedence.c: three expressions that do not group the way they read.
#include <stdio.h>

int main(void)
{
    int x = 6;
    printf("1 << 2 + 1   = %d\n", 1 << 2 + 1);   // + binds tighter than <<
    printf("x & 1 == 0   = %d\n", x & 1 == 0);   // == binds tighter than &
    printf("(x & 1) == 0 = %d\n", (x & 1) == 0);
    int n = 0;
    if (n != 0 && 10 / n > 1)                     // && stops before dividing
        puts("never printed");
    printf("short-circuit kept us from dividing by %d\n", n);
    return 0;
}
