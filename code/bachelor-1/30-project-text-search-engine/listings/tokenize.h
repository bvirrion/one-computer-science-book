// tokenize.h: splitting a text into words, and reading a whole file.
#ifndef TOKENIZE_H
#define TOKENIZE_H
#include <stddef.h>

#define MAX_WORD 64  // a longer word is cut to its first MAX_WORD - 1 letters

// The next word of text[0..len) at or after *pos: a maximal run of ASCII letters,
// lowercased into word. Returns its length, 0 when there is none left; *pos moves
// past it. Every other byte separates words, the bytes of non-ASCII letters too.
size_t next_word(const char *text, size_t len, size_t *pos, char word[MAX_WORD]);

// The whole file, in a malloc'd buffer of *len bytes (not a string); NULL on error.
char *read_file(const char *path, size_t *len);
// The words of the command-line arguments, as the tokenizer cuts them: at most max.
int split_words(int argc, char **argv, char words[][MAX_WORD], char **terms, int max);
#endif
