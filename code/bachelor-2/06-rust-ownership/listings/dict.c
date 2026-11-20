/* dict.c: count the words of standard input; print how many differ and the most frequent. */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include "dict.h"

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);
    struct dict d;
    dict_init(&d, 8);
    char *line = NULL;
    size_t size = 0;
    while (getline(&line, &size, stdin) != -1)     /* one buffer, reused for every line */
        for (char *w = strtok(line, " ,\n"); w; w = strtok(NULL, " ,\n")) {
#if BUG == 1
            int *first = dict_count(&d, "The");   /* BUG 1: a pointer kept across insertions */
            (*dict_count(&d, w))++;
            (*first) += 0;
#else
            (*dict_count(&d, w))++;
#endif
        }
    free(line);
    const char *best = NULL;                       /* borrowed from the table */
    int most = 0;
    for (size_t i = 0; i < d.cap; i++)
        if (d.slots[i].word && d.slots[i].count > most) {
            best = d.slots[i].word;
            most = d.slots[i].count;
        }
    printf("%zu different words; most frequent: %s (%d)\n", d.len, best, most);
#if BUG == 2
    free((char *)best);                     /* BUG 2: the caller frees a word the table owns */
#endif
    dict_free(&d);
    return 0;
}
