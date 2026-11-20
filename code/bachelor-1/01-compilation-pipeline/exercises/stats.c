// stats.c: the implementation of the statistics module (exercise 7).
#include "stats.h"

double mean(const double *x, size_t n)
{
    double s = 0;
    for (size_t i = 0; i < n; i++)
        s += x[i];
    return n ? s / n : 0.0;
}

double maximum(const double *x, size_t n)
{
    double m = x[0];
    for (size_t i = 1; i < n; i++)
        if (x[i] > m)
            m = x[i];
    return m;
}
