// loans.h: the town's 400 loans (data/town/loans.csv): book, day out and day returned,
// counted in days from 1 January 2025; returned is -1 for a book not yet returned.
#ifndef LOANS_H
#define LOANS_H
#include <stdio.h>
#include <stdlib.h>

enum { LOANS = 400 };
typedef struct {
    int book, out, returned;
} loan;
static loan loans[LOANS];

static int day_number(int y, int m, int d) {  // 2025 and 2026 are not leap years
    static const int before[] = {0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334};
    return 365 * (y - 2025) + before[m - 1] + d - 1;
}

static void read_loans(void) {
    FILE *f = fopen("../../../../data/town/loans.csv", "r");
    if (f == NULL) {
        perror("loans.csv");
        exit(1);
    }
    char line[128];
    int id, book, member, y, m, d, y2, m2, d2, n = 0;
    if (fgets(line, sizeof line, f) == NULL) exit(1);  // the header
    while (n < LOANS && fgets(line, sizeof line, f) != NULL) {
        int k = sscanf(line, "%d,%d,%d,%d-%d-%d,%*d-%*d-%*d,%d-%d-%d", &id, &book, &member, &y, &m,
                       &d, &y2, &m2, &d2);
        if (k < 6) continue;
        loans[n++] = (loan){book, day_number(y, m, d), k == 9 ? day_number(y2, m2, d2) : -1};
    }
    fclose(f);
}
#endif
