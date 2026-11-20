// test-with: ../listings/date.c ../listings/csv.c ../listings/loans.c
// The date tests of the weekend problem, and tests of the csv and loans modules.
#include <string.h>
#include "check.h"
#include "csv.h"
#include "date.h"
#include "loans.h"

int main(void)
{
    CHECK(!is_leap(1900) && !is_leap(2100) && is_leap(2000) && is_leap(2024) && !is_leap(2025));
    struct date a, b;
    CHECK(date_parse("2024-02-29", &a) == 0 && date_parse("2025-02-29", &b) == -1);
    CHECK(date_parse("2099-02-28", &a) == 0 && date_parse("2100-03-01", &b) == 0 && days_between(a, b) == 366);
    char line[] = "1,59,41,2025-01-01,2025-01-22,\n";
    char *f[6];
    CHECK(csv_split(line, f, 6) == 6 && strcmp(f[3], "2025-01-01") == 0 && f[5][0] == '\0');
    char too_many[] = "a,b,c";
    CHECK(csv_split(too_many, f, 2) == -1);
    char l1[] = "1,59,41,2025-01-01,2025-01-22,2025-01-30\n";
    struct loan l;
    struct date today = {2025, 12, 31};
    CHECK(loan_parse(l1, &l) == 0 && l.returned && loan_days_late(&l, today) == 8);
    char l2[] = "2,73,8,2025-12-01,2025-12-22,\n";
    CHECK(loan_parse(l2, &l) == 0 && !l.returned && loan_days_late(&l, today) == 9);
    char l3[] = "3,73,8,2025-12-01,2025-12-22,2025-12-20\n";
    CHECK(loan_parse(l3, &l) == 0 && loan_days_late(&l, today) == 0);
    char bad[] = "4,73,8,2025-12-01,2025-13-22,\n";
    CHECK(loan_parse(bad, &l) == -1);
    return CHECK_REPORT();
}
