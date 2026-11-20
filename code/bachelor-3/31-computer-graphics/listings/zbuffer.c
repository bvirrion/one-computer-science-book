// zbuffer.c -- two triangles that cross each other, drawn with a depth buffer: each
// pixel keeps the nearest surface. Depth is interpolated with barycentric weights.
#include <stdio.h>

#include "ppm.h"
#include "raster.h"

#define W 160
#define H 120

typedef struct { double x, y, z; } vertex;  // pixel coordinates and a depth in [0, 1]

static double depth[H][W], image[H][W][3];
static int covers[H][W], front[H][W];  // which triangles cover a pixel; which one won

static void draw(int id, vertex v[3], const double colour[3]) {
    vertex u[3] = {v[0], v[1], v[2]};
    pt a = fixed(u[0].x, u[0].y), b = fixed(u[1].x, u[1].y), c = fixed(u[2].x, u[2].y);
    if (edge(a, b, c) < 0) {  // clockwise order; each depth stays with its vertex
        pt t = b;
        b = c, c = t;
        vertex s = u[1];
        u[1] = u[2], u[2] = s;
    }
    double area = (double)edge(a, b, c);
    for (int j = 0; j < H; j++)
        for (int i = 0; i < W; i++) {
            pt p = centre(i, j);
            if (!inside(a, b, c, p, 1)) continue;
            double l0 = edge(b, c, p) / area, l1 = edge(c, a, p) / area, l2 = 1 - l0 - l1;
            double z = l0 * u[0].z + l1 * u[1].z + l2 * u[2].z;  // barycentric depth
            covers[j][i] |= id;
            if (z < depth[j][i]) {  // nearer than what is there: draw it
                depth[j][i] = z, front[j][i] = id;
                for (int k = 0; k < 3; k++) image[j][i][k] = colour[k] * (1.1 - z);
            }
        }
}

int main(void) {
    for (int j = 0; j < H; j++)
        for (int i = 0; i < W; i++) {
            depth[j][i] = 1.0;  // the far plane: anything drawn is nearer
            for (int k = 0; k < 3; k++) image[j][i][k] = 0.92;
        }
    vertex red[3] = {{10, 15, 0.2}, {150, 40, 0.8}, {40, 110, 0.2}};
    vertex blue[3] = {{20, 60, 0.7}, {120, 8, 0.3}, {140, 112, 0.3}};
    draw(1, red, (double[]){0.85, 0.2, 0.15});
    draw(2, blue, (double[]){0.15, 0.3, 0.85});
    int count[4] = {0}, red_front = 0;
    for (int j = 0; j < H; j++)
        for (int i = 0; i < W; i++) {
            count[covers[j][i]]++;
            red_front += covers[j][i] == 3 && front[j][i] == 1;
        }
    printf("pixels covered by red only %d, blue only %d, both %d, neither %d\n", count[1],
           count[2], count[3], count[0]);
    printf("where both cover a pixel: red in front at %d, blue at %d\n", red_front,
           count[3] - red_front);
    return write_ppm("../figures/zbuffer.ppm", W, H, &image[0][0][0]) ? 1 : 0;
}
