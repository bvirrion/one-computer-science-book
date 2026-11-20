// loans.c: parsing a loan, and counting late days.
#include <stdlib.h>
#include "csv.h"
#include "loans.h"

int loan_parse(char *line, struct loan *l)
{
    char *f[6];
    if (csv_split(line, f, 6) != 6)
        return -1;
    l->id = atoi(f[0]);
    l->book = atoi(f[1]);
    l->member = atoi(f[2]);
    if (date_parse(f[3], &l->out) != 0 || date_parse(f[4], &l->due) != 0)
        return -1;
    l->returned = f[5][0] != '\0';
    if (l->returned && date_parse(f[5], &l->back) != 0)
        return -1;
    return 0;
}

long loan_days_late(const struct loan *l, struct date today)
{
    long late = days_between(l->due, l->returned ? l->back : today);
    return late > 0 ? late : 0;
}
