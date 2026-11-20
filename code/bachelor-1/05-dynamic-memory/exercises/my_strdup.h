// my_strdup.h: a heap copy of a string (exercise 7).
#ifndef MY_STRDUP_H
#define MY_STRDUP_H

// Returns a new heap block holding a copy of s, or NULL if out of memory.
// The caller owns the copy and must free it.
char *my_strdup(const char *s);

#endif
