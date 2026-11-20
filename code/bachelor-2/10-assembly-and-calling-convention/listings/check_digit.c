/* check_digit.c: the library's check digit, the function the problem compiles by hand. */
#include <stdio.h>

unsigned weigh(unsigned digit, unsigned i)
{
    return digit * (i % 2 == 0 ? 3 : 1);     /* weight 3 at even positions from the right */
}

unsigned check_digit(unsigned code)
{
    unsigned sum = 0, i = 0;
    do {                                      /* a code has at least one digit */
        sum += weigh(code % 10, i);
        code /= 10;
        i++;
    } while (code != 0);
    return (10 - sum % 10) % 10;
}

int main(void)
{
    unsigned codes[] = {7, 4006, 9780306, 978030640};
    for (int k = 0; k < 4; k++)
        printf("%u -> %u\n", codes[k], check_digit(codes[k]));
    return 0;
}
