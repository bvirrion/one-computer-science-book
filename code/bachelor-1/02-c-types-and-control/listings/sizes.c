// sizes.c: the widths and limits of the integer types on this machine.
#include <limits.h>
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    printf("char       %zu byte,  %d .. %d\n", sizeof(char), CHAR_MIN, CHAR_MAX);
    printf("short      %zu bytes, %d .. %d\n", sizeof(short), SHRT_MIN, SHRT_MAX);
    printf("int        %zu bytes, %d .. %d\n", sizeof(int), INT_MIN, INT_MAX);
    printf("long       %zu bytes, %ld .. %ld\n", sizeof(long), LONG_MIN, LONG_MAX);
    printf("long long  %zu bytes\n", sizeof(long long));
    printf("unsigned   %zu bytes, 0 .. %u\n", sizeof(unsigned), UINT_MAX);
    printf("int8_t %zu, int16_t %zu, int32_t %zu, int64_t %zu\n", sizeof(int8_t),
           sizeof(int16_t), sizeof(int32_t), sizeof(int64_t));
    printf("a pointer  %zu bytes, size_t %zu bytes\n", sizeof(void *), sizeof(size_t));
    return 0;
}
