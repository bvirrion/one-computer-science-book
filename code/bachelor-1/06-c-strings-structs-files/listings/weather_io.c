// weather_io.c: robust parsing of the town's CSV, and a portable packed format.
#include <errno.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include "weather.h"

static int field_double(const char *s, const char *stop, double *v)
{
    char *end;
    errno = 0;
    *v = strtod(s, &end);
    return (end == s || end != stop || errno == ERANGE) ? -1 : 0;
}

int parse_reading(const char *line, struct reading *r)
{
    const char *f[5];                                   // the start of each field
    f[0] = line;
    for (int i = 1; i < 5; i++) {
        const char *comma = strchr(f[i - 1], ',');
        if (comma == NULL)
            return -1;
        f[i] = comma + 1;
    }
    int y, m, d;
    if (sscanf(f[0], "%4d-%2d-%2d,", &y, &m, &d) != 3)
        return -1;
    r->date = y * 10000 + m * 100 + d;
    r->station = f[1][0];
    r->flag = 0;
    r->temp = 0.0;
    double v;
    if (f[2][0] == ',')
        r->flag = TEMP_MISSING;
    else if (field_double(f[2], f[3] - 1, &v) != 0)
        return -1;
    else if (v == -99.0)
        r->flag = TEMP_ERROR;
    else
        r->temp = v;
    if (field_double(f[3], f[4] - 1, &v) != 0)
        return -1;
    r->rain = (float)v;
    char *end;
    r->wind = strtof(f[4], &end);
    return (end == f[4] || (*end != '\n' && *end != '\0')) ? -1 : 0;
}

int read_weather(FILE *f, struct reading *r, int max, int *lines, int *duplicates)
{
    char line[128], previous[128] = "";
    int n = 0;
    *lines = *duplicates = 0;
    if (fgets(line, sizeof line, f) == NULL)            // the header
        return -1;
    while (n < max && fgets(line, sizeof line, f) != NULL) {
        ++*lines;
        if (strcmp(line, previous) == 0) {
            ++*duplicates;
            continue;
        }
        strcpy(previous, line);
        if (parse_reading(line, &r[n]) != 0)
            return -1;
        n++;
    }
    return n;
}

static void put(unsigned char *p, uint32_t v, int n)
{
    for (int i = 0; i < n; i++)
        p[i] = (unsigned char)(v >> (8 * i));
}

static uint32_t get(const unsigned char *p, int n)
{
    uint32_t v = 0;
    for (int i = 0; i < n; i++)
        v |= (uint32_t)p[i] << (8 * i);
    return v;
}

void pack_reading(const struct reading *r, unsigned char out[PACKED_BYTES])
{
    put(out, (uint32_t)r->date, 4);
    out[4] = (unsigned char)r->station;
    out[5] = (unsigned char)r->flag;
    put(out + 6, (uint16_t)(int16_t)lround(r->temp * 10), 2);
    put(out + 8, (uint16_t)lround(r->rain * 10), 2);
    put(out + 10, (uint16_t)lround(r->wind * 10), 2);
}

void unpack_reading(const unsigned char in[PACKED_BYTES], struct reading *r)
{
    r->date = (int32_t)get(in, 4);
    r->station = (char)in[4];
    r->flag = (char)in[5];
    r->temp = (int16_t)get(in + 6, 2) / 10.0;
    r->rain = (float)(get(in + 8, 2) / 10.0);
    r->wind = (float)(get(in + 10, 2) / 10.0);
}
