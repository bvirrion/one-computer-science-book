/* fines_tables_test.c: the C tables of exercise 7 give the fines of the switch. */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "../exercises/fines_tables.h"

static int switch_fine(int kind, int d)            /* fines_switch.c, kinds 0, 1, 2 */
{
    if (d <= 0) return 0;
    switch (kind) {
    case 0: return d * 10 < 500 ? d * 10 : 500;
    case 1: return d * 25 < 300 ? d * 25 : 300;
    default: return d > 3 ? (d - 3) * 20 : 0;
    }
}

int main(void)
{
    const struct kind_table *kinds[] = {&STANDARD, &COMIC, &STUDY};
    for (int k = 0; k < 3; k++)
        for (int d = -2; d <= 400; d++) {
            struct item it = {"x", kinds[k]};
            assert(fine_cents(&it, d) == switch_fine(k, d));
        }
    assert(strcmp(COMIC.name, "comic") == 0);
    puts("fines_tables_test: OK");
    return 0;
}
