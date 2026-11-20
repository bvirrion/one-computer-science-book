// keyvalue.h: read key=value lines into an array of structures (exercise 8).
#ifndef KEYVALUE_H
#define KEYVALUE_H
#include <stdio.h>

struct setting {
    char key[32];
    char value[64];
};

// Reads lines "key=value" from f into s[0..max-1], ignoring empty lines and lines starting with '#'.
// Returns the number of settings read, or -1 at the first malformed line (no '=', empty key, or a key
// or value too long), with *bad_line set to its number (from 1).
int read_settings(FILE *f, struct setting *s, int max, int *bad_line);

#endif
