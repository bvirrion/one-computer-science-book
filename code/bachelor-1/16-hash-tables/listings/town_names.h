// town_names.h: the full names of the town's 120 people, read from data/town/people.csv.
#ifndef TOWN_NAMES_H
#define TOWN_NAMES_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { PEOPLE = 120 };
static char town_names[PEOPLE][80];

static void read_town_names(void) {
    FILE *f = fopen("../../../../data/town/people.csv", "r");
    if (f == NULL) {
        perror("people.csv");
        exit(1);
    }
    char line[128], first[39], last[39];
    int id, year, street, n = 0;
    if (fgets(line, sizeof line, f) == NULL) exit(1);  // the header
    while (n < PEOPLE && fgets(line, sizeof line, f) != NULL)
        if (sscanf(line, "%d,%38[^,],%38[^,],%d,%d", &id, first, last, &year, &street) == 5)
            snprintf(town_names[n++], sizeof town_names[0], "%s %s", first, last);
    fclose(f);
}
#endif
