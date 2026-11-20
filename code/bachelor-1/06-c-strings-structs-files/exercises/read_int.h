// read_int.h: a strict conversion of a line to an int (exercise 12).
#ifndef READ_INT_H
#define READ_INT_H

// Converts s (optional spaces, an optional sign, digits, optional spaces, an optional final newline)
// to an int in *out. Returns 0, or -1 for an empty string, a non-number, trailing characters, or a value
// outside the range of int. *out is changed only on success.
int read_int(const char *s, int *out);

#endif
