// str_append.h: a bounded string append (exercise 7).
#ifndef STR_APPEND_H
#define STR_APPEND_H
#include <stddef.h>

// dst holds a string in a buffer of cap bytes. Appends as much of src as fits, always ends dst with a zero
// byte, and returns 0 if all of src was appended, -1 if it was truncated (or if cap == 0).
int str_append(char *dst, size_t cap, const char *src);

#endif
