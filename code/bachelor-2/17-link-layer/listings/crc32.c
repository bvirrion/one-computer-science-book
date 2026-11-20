/* crc32.c: the table-driven CRC-32, in C; its values are zlib's. */
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static uint32_t table[256];

static void make_table(void)
{
    for (uint32_t b = 0; b < 256; b++) {
        uint32_t c = b;
        for (int k = 0; k < 8; k++)
            c = c & 1 ? (c >> 1) ^ 0xEDB88320u : c >> 1;
        table[b] = c;
    }
}

uint32_t crc32(const unsigned char *data, size_t n)
{
    uint32_t crc = 0xFFFFFFFFu;
    for (size_t i = 0; i < n; i++)
        crc = table[(crc ^ data[i]) & 0xFF] ^ (crc >> 8);
    return crc ^ 0xFFFFFFFFu;
}

int main(void)
{
    const char *inputs[] = {"", "a", "123456789", "LAMP ON AT 20:00"};
    make_table();
    for (int i = 0; i < 4; i++)
        printf("%08x  \"%s\"\n", crc32((const unsigned char *)inputs[i], strlen(inputs[i])),
               inputs[i]);
    return 0;
}
