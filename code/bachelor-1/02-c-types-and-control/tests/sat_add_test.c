// test-with: ../exercises/sat_add.c
#include <assert.h>
#include <stdio.h>
#include "../exercises/sat_add.h"

int main(void)
{
    assert(sat_add(2, 3) == 5);
    assert(sat_add(INT32_MAX, 1) == INT32_MAX);
    assert(sat_add(INT32_MAX, INT32_MAX) == INT32_MAX);
    assert(sat_add(INT32_MIN, -1) == INT32_MIN);
    assert(sat_add(INT32_MIN, INT32_MAX) == -1);
    assert(sat_add(-5, 5) == 0);
    for (int64_t a = -70000; a <= 70000; a += 997)
        for (int64_t b = INT32_MAX - 3; b > INT32_MAX - 300000; b -= 7919) {
            int64_t exact = a + b;
            int64_t want = exact > INT32_MAX ? INT32_MAX : exact < INT32_MIN ? INT32_MIN : exact;
            assert(sat_add((int32_t)a, (int32_t)b) == want);
            assert(sat_add((int32_t)-a, (int32_t)-b) == (want == INT32_MAX ? INT32_MIN + 1 : -want)
                   || sat_add((int32_t)-a, (int32_t)-b) == INT32_MIN);
        }
    puts("sat_add_test: ok");
    return 0;
}
