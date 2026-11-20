// exo_assert.c: a precondition, checked.
#include <assert.h>
#include <stdio.h>

int percent(int part, int whole)
{
    assert(whole > 0 && part >= 0 && part <= whole);
    return 100 * part / whole;
}

int main(void)
{
    printf("%d%%\n", percent(87, 400));
    printf("%d%%\n", percent(22, 0));
    return 0;
}
