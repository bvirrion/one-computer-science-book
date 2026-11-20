// test-with: date.c
// date_test.c: tests of the date module, chosen by input classes and boundaries.
#include "check.h"
#include "date.h"

static long between(const char *a, const char *b)
{
    struct date x, y;
    if (date_parse(a, &x) != 0 || date_parse(b, &y) != 0)
        return -999999;
    return days_between(x, y);
}

int main(void)
{
    CHECK(!is_leap(2025) && is_leap(2024));            // ordinary years
    CHECK(!is_leap(1900) && !is_leap(2100));           // centuries
    CHECK(is_leap(2000) && is_leap(2400));             // every fourth century
    CHECK(days_in_month(2025, 2) == 28 && days_in_month(2024, 2) == 29);
    CHECK(days_in_month(2025, 1) == 31 && days_in_month(2025, 12) == 31 && days_in_month(2025, 4) == 30);
    struct date d;
    CHECK(date_parse("2025-06-14", &d) == 0 && d.year == 2025 && d.month == 6 && d.day == 14);
    CHECK(date_parse("2025-02-29", &d) == -1);         // not a leap year
    CHECK(date_parse("2024-02-29", &d) == 0);
    CHECK(date_parse("2025-13-01", &d) == -1 && date_parse("2025-00-10", &d) == -1);
    CHECK(date_parse("2025-04-31", &d) == -1 && date_parse("2025-04-00", &d) == -1);
    CHECK(date_parse("1969-12-31", &d) == -1);         // before the domain
    CHECK(date_parse("2025-06-14x", &d) == -1 && date_parse("2025-06", &d) == -1);
    CHECK(between("2025-01-22", "2025-01-22") == 0);
    CHECK(between("2025-01-22", "2025-01-03") == -19);
    CHECK(between("2025-12-31", "2026-01-01") == 1);   // across a year
    CHECK(between("2024-02-28", "2024-03-01") == 2);   // across a leap day
    CHECK(between("1970-01-01", "2000-01-01") == 10957);
    CHECK(between("2099-02-28", "2100-03-01") == 366); // 2100 is not a leap year
    return CHECK_REPORT();
}
