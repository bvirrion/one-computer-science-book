// sort_people.c: qsort with three comparators, on people of the town (data/town/people.csv).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int increasing(const void *x, const void *y)     // qsort passes the addresses of two elements
{
    int a = *(const int *)x, b = *(const int *)y;
    return (a > b) - (a < b);                    // negative, zero or positive
}

int decreasing(const void *x, const void *y)
{
    return increasing(y, x);
}

int alphabetical(const void *x, const void *y)   // the elements are pointers to characters
{
    return strcmp(*(const char *const *)x, *(const char *const *)y);
}

int main(void)
{
    int born[] = {1967, 1986, 1963, 2002, 2010, 1951, 2007, 1962};
    const char *first[] = {"Emil", "Quinn", "Rosa", "Sami", "Vera", "Nils", "Caio", "Farid"};
    size_t n = sizeof born / sizeof born[0];
    qsort(born, n, sizeof born[0], increasing);
    for (size_t i = 0; i < n; i++)
        printf("%d%c", born[i], i + 1 < n ? ' ' : '\n');
    qsort(born, n, sizeof born[0], decreasing);
    for (size_t i = 0; i < n; i++)
        printf("%d%c", born[i], i + 1 < n ? ' ' : '\n');
    qsort(first, n, sizeof first[0], alphabetical);
    for (size_t i = 0; i < n; i++)
        printf("%s%c", first[i], i + 1 < n ? ' ' : '\n');
    return 0;
}
