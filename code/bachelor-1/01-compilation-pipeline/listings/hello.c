// hello.c: one small program, followed through the four stages.
#include <stdio.h>

#define GREETING "Hello from C"
#define SQUARE(x) ((x) * (x))

int main(void)
{
    int n = 7;
    printf("%s: %d squared is %d\n", GREETING, n, SQUARE(n));
    return 0;
}
