// wrap.c: unsigned arithmetic is arithmetic modulo 2 to the power N.
#include <limits.h>
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    uint8_t small = 250;
    small = small + 10;                  // 260 mod 256
    unsigned big = UINT_MAX;
    big = big + 1;                       // 2^32 mod 2^32
    unsigned below = 0;
    below = below - 1;                   // -1 mod 2^32
    printf("250 + 10 in 8 bits     = %u\n", (unsigned)small);
    printf("UINT_MAX + 1           = %u\n", big);
    printf("0 - 1 in unsigned int  = %u\n", below);
    return 0;
}
