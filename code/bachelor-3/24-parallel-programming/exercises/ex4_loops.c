/* ex4_loops.c -- three loops: which does gcc -O3 vectorize? */
void ahead(int n, float *y)                     /* (a) */
{
    for (int i = 0; i < n - 1; i++)
        y[i] = 2 * y[i + 1];
}

void behind4(int n, float *restrict y, const float *restrict x)  /* (b) */
{
    for (int i = 4; i < n; i++)
        y[i] = y[i - 4] + x[i];
}

void behind1(int n, float *restrict y, const float *restrict x)  /* (c) */
{
    for (int i = 1; i < n; i++)
        y[i] = y[i - 1] + x[i];
}
