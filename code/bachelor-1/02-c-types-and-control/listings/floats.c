// floats.c: binary fractions are rounded; compare them with a tolerance.
#include <math.h>
#include <stdio.h>

int nearly_equal(double a, double b, double rel)
{
    return fabs(a - b) <= rel * fmax(fabs(a), fabs(b));
}

int main(void)
{
    double s = 0.1 + 0.2;
    printf("0.1 + 0.2 = %.17g\n", s);
    printf("s == 0.3 gives %d\n", s == 0.3);
    printf("nearly_equal(s, 0.3) gives %d\n", nearly_equal(s, 0.3, 1e-12));
    char letter = 'A';
    printf("'A' is the integer %d, 'A' + 2 is '%c'\n", letter, letter + 2);
    return 0;
}
