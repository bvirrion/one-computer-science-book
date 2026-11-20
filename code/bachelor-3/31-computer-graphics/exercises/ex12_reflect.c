// Exercise 12: reflections. The same scene, each sphere a partial mirror; the reflected
// ray is traced recursively up to a depth limit, and every ray is counted.
#include <stdio.h>

#include "ppm.h"
#include "rt.h"

#define W 320
#define H 240
#define PI 3.14159265358979323846

// Traces the whole image with the given depth limit; image may be NULL.
static counts render(int limit, double *image) {
    counts n = {0};
    double half = tan(PI / 6);
    for (int j = 0; j < H; j++)
        for (int i = 0; i < W; i++) {
            double x = (2 * (i + 0.5) / W - 1) * half * W / H;
            double y = (1 - 2 * (j + 0.5) / H) * half;
            n.primary++;
            vec3 c = trace(v3(0, 0, 0), unit(v3(x, y, -1)), limit, &n);
            if (image) {
                double *px = image + 3 * ((long)j * W + i);
                px[0] = c.x, px[1] = c.y, px[2] = c.z;
            }
        }
    return n;
}

#ifndef NO_MAIN
int main(void) {
    static double image[H * W * 3];
    for (int limit = 0; limit <= 4; limit++) {
        counts n = render(limit, limit == 3 ? image : NULL);
        printf("depth limit %d: primary %ld, reflected %ld, shadow %ld, total %ld rays\n",
               limit, n.primary, n.reflected, n.shadow, n.primary + n.reflected + n.shadow);
    }
    return write_ppm("../figures/reflect.ppm", W, H, image) ? 1 : 0;
}
#endif
