// Exercise 5: a spinning cube that drifts. The buggy model matrix translates first and
// rotates second, so the cube's centre circles around the camera's axis instead of
// staying 6 units in front of it.
#include <stdio.h>

#include "vec.h"

#define PI 3.14159265358979323846

static double tidy(double x) { return fabs(x) < 0.005 ? 0 : x; }  // no "-0.00"

int main(void) {
    for (int frame = 0; frame <= 4; frame++) {
        double a = frame * PI / 4;
        mat4 buggy = matmul(rotate_y(a), translate(0, 0, -6));  // translate, then rotate
        mat4 fixed = matmul(translate(0, 0, -6), rotate_y(a));  // rotate, then translate
        vec4 o = {0, 0, 0, 1};
        vec4 b = apply(buggy, o), f = apply(fixed, o);
        printf("angle %3d: centre buggy (%5.2f, %5.2f, %5.2f), fixed (%5.2f, %5.2f, %5.2f)\n",
               frame * 45, tidy(b.x), tidy(b.y), tidy(b.z), tidy(f.x), tidy(f.y), tidy(f.z));
    }
    return 0;
}
