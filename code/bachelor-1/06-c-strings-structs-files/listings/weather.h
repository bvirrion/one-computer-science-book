// weather.h: one day of one station, in memory and in the archive files.
#ifndef WEATHER_H
#define WEATHER_H
#include <stdint.h>
#include <stdio.h>

enum { TEMP_MISSING = 1, TEMP_ERROR = 2 };             // bits of the flag field

struct reading_first {                                  // the fields in the order of the CSV
    int32_t date;                                       // 20250614
    char station;                                       // 'H' or 'R'
    double temp;                                        // degrees Celsius
    char flag;
    float rain, wind;                                   // millimetres, km/h
};

struct reading {                                        // the same fields, by decreasing alignment
    double temp;
    int32_t date;
    float rain, wind;
    char station;
    char flag;
};

#define PACKED_BYTES 12     // date 4, station 1, flag 1, temp, rain, wind in tenths: 2 each

// Parses one CSV line. Returns 0, or -1 if the line is malformed.
int parse_reading(const char *line, struct reading *r);
// Reads the whole file (header first); skips a line equal to the previous one. Returns the number of
// readings stored in r[0..max-1], or -1. *lines, *duplicates count the data lines and the skipped ones.
int read_weather(FILE *f, struct reading *r, int max, int *lines, int *duplicates);
void pack_reading(const struct reading *r, unsigned char out[PACKED_BYTES]);
void unpack_reading(const unsigned char in[PACKED_BYTES], struct reading *r);

#endif
