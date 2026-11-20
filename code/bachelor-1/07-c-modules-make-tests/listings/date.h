// date.h: calendar dates of the Gregorian calendar, from 1970 on.
#ifndef DATE_H
#define DATE_H

struct date {
    int year, month, day;
};

int is_leap(int year);
int days_in_month(int year, int month);              // month from 1 to 12
int date_parse(const char *s, struct date *d);       // "YYYY-MM-DD", year >= 1970: 0, or -1
long days_between(struct date a, struct date b);     // b - a, in days

#endif
