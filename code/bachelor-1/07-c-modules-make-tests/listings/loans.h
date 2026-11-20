// loans.h: one loan of the town library, and how late it is.
#ifndef LOANS_H
#define LOANS_H
#include "date.h"

struct loan {
    int id, book, member;
    struct date out, due, back;
    int returned;                                    // 0 while the book is out
};

int loan_parse(char *line, struct loan *l);          // a line of loans.csv: 0, or -1
long loan_days_late(const struct loan *l, struct date today);   // 0 if not late

#endif
