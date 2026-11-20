// fines_switch.c: the library's late fines in C, one switch on a kind tag.
#include <stdio.h>

enum kind { STANDARD, COMIC, STUDY };

struct item {
    const char *title;
    enum kind kind;
};

int fine_cents(const struct item *it, int days_late)    // fine for one late loan
{
    if (days_late <= 0)
        return 0;
    switch (it->kind) {
    case STANDARD:                                      // 10 cents a day, at most 5.00
        return days_late * 10 < 500 ? days_late * 10 : 500;
    case COMIC:                                         // 25 cents a day, at most 3.00
        return days_late * 25 < 300 ? days_late * 25 : 300;
    case STUDY:                                         // 3 days of grace, then 20 a day
        return days_late > 3 ? (days_late - 3) * 20 : 0;
    }
    return 0;
}

const char *kind_name(enum kind k)                      // a second switch on the same tag
{
    switch (k) {
    case STANDARD: return "standard";
    case COMIC:    return "comic";
    case STUDY:    return "study";
    }
    return "?";
}

int main(void)
{
    struct item items[] = {{"The Silent Code", STANDARD}, {"A Year by the Island", COMIC},
                           {"Tides and Moons", STUDY}};
    int late[] = {2, 10, 60};
    for (int i = 0; i < 3; i++) {
        printf("%-22s %-9s", items[i].title, kind_name(items[i].kind));
        for (int j = 0; j < 3; j++)
            printf("  %2d days: %5.2f", late[j], fine_cents(&items[i], late[j]) / 100.0);
        printf("\n");
    }
    return 0;
}
