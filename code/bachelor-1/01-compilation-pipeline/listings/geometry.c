// geometry.c: a small module whose object file the exercise reads.
#include <math.h>

double scale = 2.0;
long calls;
static int last_sign;

double hypotenuse(double a, double b)
{
    calls++;
    last_sign = a < 0 || b < 0;
    return scale * sqrt(a * a + b * b);
}
