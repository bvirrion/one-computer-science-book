// test-with: ../exercises/record_io.c
#include <assert.h>
#include <stdio.h>
#include "../exercises/record_io.h"

int main(void)
{
    struct record r = {20250614, -35, 123}, back;
    unsigned char b[RECORD_BYTES];
    record_encode(&r, b);
    // 20250614 = 0x0134FFF6, -35 = 0xFFDD, 123 = 0x007B, least significant byte first
    unsigned char expected[RECORD_BYTES] = {0xF6, 0xFF, 0x34, 0x01, 0xDD, 0xFF, 0x7B, 0x00};
    for (int i = 0; i < RECORD_BYTES; i++)
        assert(b[i] == expected[i]);
    FILE *f = tmpfile();
    for (int i = 0; i < 100; i++) {
        struct record w = {20250101 + (uint32_t)i, (int16_t)(i * 7 - 300), (uint16_t)(i * 13)};
        assert(record_write(f, &w) == 0);
    }
    assert(ftell(f) == 100 * RECORD_BYTES);
    rewind(f);
    for (int i = 0; i < 100; i++) {
        assert(record_read(f, &back) == 0);
        assert(back.date == 20250101 + (uint32_t)i && back.temp == i * 7 - 300 && back.rain == i * 13);
    }
    assert(record_read(f, &back) == -1);
    fclose(f);
    puts("record_io_test: ok");
    return 0;
}
