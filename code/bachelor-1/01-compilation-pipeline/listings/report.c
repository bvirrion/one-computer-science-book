// report.c: prints the counts, at most MAX_REPORTS times.
#include <stdio.h>
#include "count.h"

const char *unit = "words";

void report(const char *title)
{
    static int reports = 0;
    if (reports >= MAX_REPORTS)
        return;
    reports++;
    printf("%s: %ld lines, %ld %s (report %d)\n", title, lines, words, unit,
           reports);
}
