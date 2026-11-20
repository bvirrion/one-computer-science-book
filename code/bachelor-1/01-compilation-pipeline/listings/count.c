// count.c: counts lines and words, one character at a time.
#include <ctype.h>
#include "count.h"

long lines, words;
static int in_word = 0;

void feed(int c)
{
    if (c == '\n')
        lines++;
    if (isspace(c))
        in_word = 0;
    else if (!in_word) {
        in_word = 1;
        words++;
    }
}
