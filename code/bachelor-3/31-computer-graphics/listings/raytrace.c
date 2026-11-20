// raytrace.c -- the scene of rt.h traced ray by ray: one primary ray per pixel of a
// 320x240 image through a pinhole camera at the origin, and one shadow ray per hit.
#include <stdio.h>

#include "ppm.h"
#include "rt.h"

#define W 320
#define H 240
#define PI 3.14159265358979323846

static double image[H][W][3];

int main(void) {
    counts n = {0};
    double half = tan(PI / 6);  // a 60-degree vertical field of view
    for (int j = 0; j < H; j++)
        for (int i = 0; i < W; i++) {
            double x = (2 * (i + 0.5) / W - 1) * half * W / H, y = (1 - 2 * (j + 0.5) / H) * half;
            n.primary++;
            vec3 c = trace(v3(0, 0, 0), unit(v3(x, y, -1)), 0, &n);
            image[j][i][0] = c.x, image[j][i][1] = c.y, image[j][i][2] = c.z;
        }
    printf("primary rays %ld, shadow rays %ld, reflected rays %ld\n", n.primary, n.shadow,
           n.reflected);
    printf("rays ending: sky %ld, red %ld, green %ld, blue %ld, floor %ld\n", n.ends[0],
           n.ends[1], n.ends[2], n.ends[3], n.ends[4]);
    return write_ppm("../figures/raytrace.ppm", W, H, &image[0][0][0]) ? 1 : 0;
}
