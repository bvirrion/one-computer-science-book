// transform.c -- the eight corners of a cube through the model, view and projection
// transforms, the perspective division, and the viewport, to pixels of a 320x240 image.
#include <stdio.h>

#include "vec.h"

#define PI 3.14159265358979323846

int main(void) {
    mat4 model = matmul(translate(0, 0, -6), matmul(rotate_y(PI / 6), rotate_x(PI / 9)));
    mat4 view = identity();  // the camera stays at the origin, looking down -z
    mat4 proj = perspective(PI / 3, 4.0 / 3.0, 1, 20);
    mat4 mvp = matmul(proj, matmul(view, model));
    printf("corner        clip (x, y, z, w)               NDC (x, y, z)        pixel\n");
    for (int i = 0; i < 8; i++) {
        vec4 p = {i & 1 ? 1 : -1, i & 2 ? 1 : -1, i & 4 ? 1 : -1, 1};
        vec4 c = apply(mvp, p);
        double nx = c.x / c.w, ny = c.y / c.w, nz = c.z / c.w;  // perspective division
        double px = (nx + 1) / 2 * 320, py = (1 - ny) / 2 * 240;  // viewport: y down
        printf("(%2.0f,%2.0f,%2.0f)  (%6.3f,%6.3f,%6.3f,%6.3f)  (%6.3f,%6.3f,%6.3f)  (%5.1f,%5.1f)\n",
               p.x, p.y, p.z, c.x, c.y, c.z, c.w, nx, ny, nz, px, py);
    }
    return 0;
}
