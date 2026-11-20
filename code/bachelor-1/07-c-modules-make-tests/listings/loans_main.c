// loans_main.c: the library's loan checker.
#include <stdio.h>
#include "loans.h"

int main(int argc, char *argv[])
{
    struct date today;
    if (argc != 3 || date_parse(argv[2], &today) != 0) {
        fprintf(stderr, "usage: %s LOANS.CSV YYYY-MM-DD\n", argv[0]);
        return 2;
    }
    FILE *f = fopen(argv[1], "r");
    if (f == NULL) {
        perror(argv[1]);
        return 1;
    }
    char line[256];
    long late_by_member[1000] = {0};
    int loans = 0, out = 0, late = 0, worst = 0;
    long total = 0;
    if (fgets(line, sizeof line, f) == NULL)         // the header
        return 1;
    while (fgets(line, sizeof line, f) != NULL) {
        struct loan l;
        if (loan_parse(line, &l) != 0 || l.member < 0 || l.member >= 1000) {
            fprintf(stderr, "bad line %d\n", loans + 2);
            return 1;
        }
        loans++;
        out += !l.returned;
        long d = loan_days_late(&l, today);
        late += d > 0;
        total += d;
        late_by_member[l.member] += d;
        if (late_by_member[l.member] > late_by_member[worst])
            worst = l.member;
    }
    fclose(f);
    printf("%d loans, %d still out, %d late, %ld late days in all\n", loans, out, late, total);
    printf("member %d has the most late days: %ld\n", worst, late_by_member[worst]);
    return 0;
}
