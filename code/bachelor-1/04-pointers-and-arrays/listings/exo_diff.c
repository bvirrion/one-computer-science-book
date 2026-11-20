// exo_diff.c: pointers into an array of double.
#include <stdio.h>

int main(void)
{
    double t[6] = {2.5, -1.0, 4.0, 0.5, 3.5, 1.5};
    double *p = t + 1, *q = &t[5];
    printf("%td %td %.1f %.1f\n", q - p, (char *)q - (char *)p, *(p + 2), p[-1]);
    return 0;
}
