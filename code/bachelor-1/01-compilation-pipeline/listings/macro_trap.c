// macro_trap.c: what the preprocessor makes of a macro without parentheses.
#include <stdio.h>

#define DOUBLE(x) x + x
#define DOUBLE_SAFE(x) ((x) + (x))

int main(void)
{
    printf("3 * DOUBLE(2)      = %d\n", 3 * DOUBLE(2));
    printf("3 * DOUBLE_SAFE(2) = %d\n", 3 * DOUBLE_SAFE(2));
    return 0;
}
