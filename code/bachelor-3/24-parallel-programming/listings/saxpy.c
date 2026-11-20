/* saxpy.c -- y = a x + y over n floats, and a running sum over n floats. */
void saxpy(int n, float a, const float *restrict x, float *restrict y)
{
    for (int i = 0; i < n; i++)
        y[i] = a * x[i] + y[i];
}

void running_sum(int n, float *y)
{
    for (int i = 1; i < n; i++)
        y[i] = y[i] + y[i - 1];
}
