// endian.c: the bytes of an int in memory, and sign extension.
#include <stdio.h>

int main(void)
{
    unsigned int x = 0x12345678;
    unsigned char *b = (unsigned char *)&x;             // read the int byte by byte
    printf("0x%08x is stored as", x);
    for (size_t i = 0; i < sizeof x; i++)
        printf(" %02x", b[i]);
    printf("\n");
    signed char s = -16;                                // the byte 0xf0
    unsigned char u = 0xf0;
    int from_s = s, from_u = u;
    printf("byte 0xf0 as signed char -> int %d = 0x%08x\n", from_s, (unsigned)from_s);
    printf("byte 0xf0 as unsigned char -> int %d = 0x%08x\n", from_u, (unsigned)from_u);
    return 0;
}
