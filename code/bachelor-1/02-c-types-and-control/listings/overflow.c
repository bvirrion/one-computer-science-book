// overflow.c: signed overflow is undefined; the sanitizer reports it.
// capture: cflags=-O0 -fsanitize=undefined
#include <limits.h>
#include <stdio.h>

int main(void)
{
    int x = INT_MAX;
    int y = x + 1;                       // undefined behaviour
    printf("INT_MAX + 1 gave %d\n", y);
    return 0;
}
