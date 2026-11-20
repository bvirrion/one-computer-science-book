// temps.c: the reading part shared by both checksum programs.
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "temps.h"

int read_temps(const char *path, uint16_t *w, int max)
{
    FILE *f = fopen(path, "r");
    if (!f)
        return -1;
    char line[128];
    int n = 0;
    if (!fgets(line, sizeof line, f)) {             // the header line
        fclose(f);
        return 0;
    }
    while (n < max && fgets(line, sizeof line, f)) {
        char *field = strchr(line, ',');            // after the date
        field = field ? strchr(field + 1, ',') : NULL;   // after the station
        double t = (field && field[1] != ',') ? atof(field + 1) : 0.0;
        int16_t tenths = (int16_t)lround(t * 10);
        w[n++] = (uint16_t)tenths;                  // two's complement bits
    }
    fclose(f);
    return n;
}
