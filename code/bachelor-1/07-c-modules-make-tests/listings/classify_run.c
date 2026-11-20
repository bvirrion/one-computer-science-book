// classify_run.c: classify every triple read from standard input.
#include <stdio.h>
#include "classify.h"

int main(void)
{
    const char *names[] = {"not a triangle", "equilateral", "isosceles", "scalene"};
    int a, b, c;
    while (scanf("%d %d %d", &a, &b, &c) == 3)
        printf("%d %d %d: %s\n", a, b, c, names[classify(a, b, c)]);
    return 0;
}
