// casts.c: four conversions to predict.
#include <stdio.h>

int main(void)
{
    unsigned char a = (unsigned char)300;
    signed char b = (signed char)200;
    int c = (int)7.99;
    int d = (int)-7.99;
    printf("%d %d %d %d\n", a, b, c, d);
    return 0;
}
