// date_v0.c: the first version, with the leap-year rule everybody remembers.
#include <assert.h>
#include <stdio.h>
#include "date.h"

int is_leap(int year)
{
    return year % 4 == 0;
}

int days_in_month(int year, int month)
{
    static const int length[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    assert(month >= 1 && month <= 12);               // the caller's duty
    return month == 2 && is_leap(year) ? 29 : length[month - 1];
}

int date_parse(const char *s, struct date *d)
{
    int y, m, dd;
    char extra;
    if (sscanf(s, "%4d-%2d-%2d%c", &y, &m, &dd, &extra) != 3)
        return -1;                                   // too few fields, or something after the day
    if (y < 1970 || m < 1 || m > 12 || dd < 1 || dd > days_in_month(y, m))
        return -1;
    *d = (struct date){y, m, dd};
    return 0;
}

static long days_since_1970(struct date d)
{
    long n = 0;
    for (int y = 1970; y < d.year; y++)
        n += is_leap(y) ? 366 : 365;
    for (int m = 1; m < d.month; m++)
        n += days_in_month(d.year, m);
    return n + d.day - 1;
}

long days_between(struct date a, struct date b)
{
    return days_since_1970(b) - days_since_1970(a);
}
