// record_io.c: shifts and masks, never the memory layout of the machine.
#include "record_io.h"

static void put(unsigned char *p, uint32_t v, int n)
{
    for (int i = 0; i < n; i++)
        p[i] = (unsigned char)(v >> (8 * i));           // least significant byte first
}

static uint32_t get(const unsigned char *p, int n)
{
    uint32_t v = 0;
    for (int i = 0; i < n; i++)
        v |= (uint32_t)p[i] << (8 * i);
    return v;
}

void record_encode(const struct record *r, unsigned char out[RECORD_BYTES])
{
    put(out, r->date, 4);
    put(out + 4, (uint16_t)r->temp, 2);                 // two's complement bits of the temperature
    put(out + 6, r->rain, 2);
}

void record_decode(const unsigned char in[RECORD_BYTES], struct record *r)
{
    r->date = get(in, 4);
    r->temp = (int16_t)get(in + 4, 2);                  // back to a signed value
    r->rain = (uint16_t)get(in + 6, 2);
}

int record_write(FILE *f, const struct record *r)
{
    unsigned char buf[RECORD_BYTES];
    record_encode(r, buf);
    return fwrite(buf, 1, RECORD_BYTES, f) == RECORD_BYTES ? 0 : -1;
}

int record_read(FILE *f, struct record *r)
{
    unsigned char buf[RECORD_BYTES];
    if (fread(buf, 1, RECORD_BYTES, f) != RECORD_BYTES)
        return -1;
    record_decode(buf, r);
    return 0;
}
