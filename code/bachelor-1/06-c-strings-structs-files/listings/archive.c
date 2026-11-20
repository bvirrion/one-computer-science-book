// archive.c: read the CSV, write three archives, read the packed one back.
#include <stddef.h>
#include <stdio.h>
#include "weather.h"

static struct reading days[1000];

static long file_size(const char *path)
{
    FILE *f = fopen(path, "rb");
    if (f == NULL)
        return -1;
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fclose(f);
    return size;
}

int main(void)
{
    FILE *in = fopen("weather.csv", "r");
    if (in == NULL) {
        perror("weather.csv");
        return 1;
    }
    int lines, dups;
    int n = read_weather(in, days, 1000, &lines, &dups);
    fclose(in);
    if (n < 0) {
        fprintf(stderr, "weather.csv: malformed\n");
        return 1;
    }
    int missing = 0, errors = 0;
    for (int i = 0; i < n; i++) {
        missing += days[i].flag == TEMP_MISSING;
        errors += days[i].flag == TEMP_ERROR;
    }
    printf("%d lines, %d duplicate, %d readings (%d missing, %d error codes)\n",
           lines, dups, n, missing, errors);
    printf("sizeof: reading_first %zu, reading %zu, packed %d\n",
           sizeof(struct reading_first), sizeof(struct reading), PACKED_BYTES);

    struct reading_first first;
    FILE *a = fopen("first.bin", "wb"), *b = fopen("reading.bin", "wb"), *c = fopen("packed.bin", "wb");
    if (a == NULL || b == NULL || c == NULL)
        return 1;
    for (int i = 0; i < n; i++) {
        first = (struct reading_first){.date = days[i].date, .station = days[i].station,
                                       .temp = days[i].temp, .flag = days[i].flag,
                                       .rain = days[i].rain, .wind = days[i].wind};
        fwrite(&first, sizeof first, 1, a);
        fwrite(&days[i], sizeof days[i], 1, b);
        unsigned char buf[PACKED_BYTES];
        pack_reading(&days[i], buf);
        fwrite(buf, 1, PACKED_BYTES, c);
    }
    fclose(a);
    fclose(b);
    fclose(c);
    printf("sizes: first.bin %ld, reading.bin %ld, packed.bin %ld\n",
           file_size("first.bin"), file_size("reading.bin"), file_size("packed.bin"));

    FILE *p = fopen("packed.bin", "rb");
    unsigned char buf[PACKED_BYTES];
    struct reading r;
    int same = 0;
    for (int i = 0; i < n && fread(buf, 1, PACKED_BYTES, p) == PACKED_BYTES; i++) {
        unpack_reading(buf, &r);
        same += r.date == days[i].date && r.station == days[i].station && r.flag == days[i].flag &&
                (long)(r.temp * 10 + (r.temp < 0 ? -0.5 : 0.5)) ==
                    (long)(days[i].temp * 10 + (days[i].temp < 0 ? -0.5 : 0.5));
    }
    fseek(p, 160 * PACKED_BYTES, SEEK_SET);             // jump straight to reading 160
    if (fread(buf, 1, PACKED_BYTES, p) == PACKED_BYTES)
        unpack_reading(buf, &r);
    fclose(p);
    printf("read back: %d of %d readings equal\n", same, n);
    printf("reading 160: %d %c %.1f C, %.1f mm, %.1f km/h\n", r.date, r.station, r.temp, r.rain, r.wind);
    return 0;
}
