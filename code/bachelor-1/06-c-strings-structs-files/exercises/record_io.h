// record_io.h: a record written byte by byte, the same on every machine (exercise 10).
#ifndef RECORD_IO_H
#define RECORD_IO_H
#include <stdint.h>
#include <stdio.h>

struct record {
    uint32_t date;                                      // 20250614
    int16_t temp;                                       // tenths of a degree
    uint16_t rain;                                      // tenths of a millimetre
};

#define RECORD_BYTES 8                                  // 4 + 2 + 2, little-endian, no padding

void record_encode(const struct record *r, unsigned char out[RECORD_BYTES]);
void record_decode(const unsigned char in[RECORD_BYTES], struct record *r);
int record_write(FILE *f, const struct record *r);      // 0, or -1
int record_read(FILE *f, struct record *r);             // 0, or -1 at the end or on error

#endif
