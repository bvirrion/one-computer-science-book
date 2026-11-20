// late_fee.c: the fee for a book returned late (exercise 8).
#include "late_fee.h"

int late_fee(int days_late, int member_years)
{
    if (days_late <= 0)
        return 0;
    int fee = 10 * days_late;
    if (days_late > 30 && member_years < 5)
        fee += 200;
    if (fee > 500)
        fee = 500;
    return fee;
}
