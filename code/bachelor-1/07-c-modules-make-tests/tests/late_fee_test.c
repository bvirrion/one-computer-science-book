// test-with: ../exercises/late_fee.c
#include "check.h"
#include "../exercises/late_fee.h"

int main(void)
{
    CHECK(late_fee(0, 1) == 0);                          // on time: first decision true
    CHECK(late_fee(3, 1) == 30);                         // a little late: both later decisions false
    CHECK(late_fee(31, 2) == 500);                       // long and new: 310 + 200, capped
    CHECK(late_fee(31, 7) == 310);                       // long but old member: && false by its right side
    CHECK(late_fee(60, 9) == 500);                       // capped without the surcharge
    CHECK(late_fee(30, 1) == 300);                       // the boundary of "more than 30"
    return CHECK_REPORT();
}
