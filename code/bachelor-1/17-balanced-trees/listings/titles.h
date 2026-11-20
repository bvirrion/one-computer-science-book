// titles.h: the 80 titles of the town library, in catalogue order (data/town/books.csv).
#ifndef TITLES_H
#define TITLES_H
#include <stdio.h>
#include <stdlib.h>

enum { TITLES = 80 };
static char titles[TITLES][40];

static void read_titles(void) {
    FILE *f = fopen("../../../../data/town/books.csv", "r");
    if (f == NULL) {
        perror("books.csv");
        exit(1);
    }
    char line[160];
    int id, n = 0;
    if (fgets(line, sizeof line, f) == NULL) exit(1);  // the header
    while (n < TITLES && fgets(line, sizeof line, f) != NULL)
        if (sscanf(line, "%d,%39[^,]", &id, titles[n]) == 2) n++;
    fclose(f);
}
#endif
