// test-with: ../exercises/generic_max.c
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "../exercises/generic_max.h"

static int cmp_int(const void *x, const void *y)
{
    int a = *(const int *)x, b = *(const int *)y;
    return (a > b) - (a < b);
}

static int cmp_double(const void *x, const void *y)
{
    double a = *(const double *)x, b = *(const double *)y;
    return (a > b) - (a < b);
}

static int cmp_word(const void *x, const void *y)
{
    return strcmp(*(const char *const *)x, *(const char *const *)y);
}

int main(void)
{
    int years[] = {1967, 2010, 1951, 2010, 1986};
    assert(generic_max(years, 5, sizeof years[0], cmp_int) == &years[1]);
    double t[] = {2.5, -1.0, 4.0, 0.5};
    assert(*(const double *)generic_max(t, 4, sizeof t[0], cmp_double) == 4.0);
    const char *names[] = {"Emil", "Vera", "Caio"};
    assert(generic_max(names, 3, sizeof names[0], cmp_word) == &names[1]);
    assert(generic_max(years, 0, sizeof years[0], cmp_int) == NULL);
    puts("generic_max_test: ok");
    return 0;
}
