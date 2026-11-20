// temps.h: read the town's daily temperatures as 16-bit words.
#ifndef TEMPS_H
#define TEMPS_H
#include <stdint.h>

// Reads the temp_c column of a weather CSV file into w[0..max-1], each value
// in tenths of a degree as an int16_t stored in a uint16_t (a missing value
// counts as 0). Returns the number of values read, or -1 on error.
int read_temps(const char *path, uint16_t *w, int max);

#endif
