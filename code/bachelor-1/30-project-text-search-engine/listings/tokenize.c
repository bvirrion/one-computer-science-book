// tokenize.c: words are runs of ASCII letters; the file is read in one buffer.
#include "tokenize.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int is_letter(unsigned char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}

size_t next_word(const char *text, size_t len, size_t *pos, char word[MAX_WORD]) {
    size_t i = *pos, n = 0;
    while (i < len && !is_letter((unsigned char)text[i]))
        i++;
    while (i < len && is_letter((unsigned char)text[i])) {
        if (n < MAX_WORD - 1)
            word[n++] = (char)(text[i] | 0x20);  // 'A'..'Z' become 'a'..'z'
        i++;
    }
    word[n] = '\0';
    *pos = i;
    return n;
}

char *read_file(const char *path, size_t *len) {
    FILE *f = fopen(path, "rb");
    if (f == NULL)
        return NULL;
    size_t cap = 4096, n = 0, got;
    char *buf = malloc(cap);
    while (buf != NULL && (got = fread(buf + n, 1, cap - n, f)) > 0) {
        n += got;
        if (n == cap) {  // full: double the buffer
            char *bigger = realloc(buf, cap *= 2);
            if (bigger == NULL)
                free(buf);
            buf = bigger;
        }
    }
    if (buf != NULL && ferror(f)) {
        free(buf);
        buf = NULL;
    }
    fclose(f);
    *len = n;
    return buf;
}

int split_words(int argc, char **argv, char words[][MAX_WORD], char **terms, int max) {
    int n = 0;
    for (int a = 0; a < argc; a++) {
        size_t pos = 0, len = strlen(argv[a]);
        while (n < max && next_word(argv[a], len, &pos, words[n]) > 0) {
            terms[n] = words[n];
            n++;
        }
    }
    return n;
}
