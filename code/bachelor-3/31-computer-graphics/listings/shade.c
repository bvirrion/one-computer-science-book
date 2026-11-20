// shade.c -- one sphere lit by one distant light, shaded twice: on the left by Gouraud
// shading (the light computed at the vertices of a coarse mesh and interpolated), on the
// right per pixel (the normal computed at every pixel). Lambert diffuse + Phong specular.
#include <stdio.h>

#include "ppm.h"
#include "raster.h"
#include "vec.h"

#define W 320
#define H 160
#define R 70.0
#define PI 3.14159265358979323846

static double image[H][W][3];
static int sphere[H][W];  // 1 where a pixel shows the sphere

// The light leaving a point of normal n towards the viewer at +z: ambient, diffuse
// (Lambert: proportional to the cosine n.L) and specular (Phong: the reflected light
// direction r against the view direction, raised to a shininess).
static vec3 light(vec3 n) {
    vec3 l = unit(v3(-1, 1, 1)), view = v3(0, 0, 1), base = v3(0.9, 0.55, 0.2);
    double diffuse = dot(n, l) > 0 ? dot(n, l) : 0;
    vec3 r = sub(mul(n, 2 * dot(n, l)), l);
    double specular = diffuse > 0 && dot(r, view) > 0 ? pow(dot(r, view), 40) : 0;
    return add(mul(base, 0.08 + 0.75 * diffuse), mul(v3(1, 1, 1), 0.6 * specular));
}

static vec3 normal_at(double u, double v) {  // longitude u, latitude v, front half
    return v3(cos(v) * sin(u), sin(v), cos(v) * cos(u));
}

static void put(int i, int j, vec3 c) {
    image[j][i][0] = c.x, image[j][i][1] = c.y, image[j][i][2] = c.z;
    sphere[j][i] = 1;
}

static double peak(int i0, int i1, int *at_i, int *at_j) {  // brightest pixel, green
    double best = -1;
    for (int j = 0; j < H; j++)
        for (int i = i0; i < i1; i++)
            if (sphere[j][i] && image[j][i][1] > best)
                best = image[j][i][1], *at_i = i, *at_j = j;
    return best;
}

int main(void) {
    for (int j = 0; j < H; j++)
        for (int i = 0; i < W; i++)
            for (int k = 0; k < 3; k++) image[j][i][k] = 0.92;  // the background
    // Gouraud: an 8 x 8 grid of the front half, two triangles per cell
    enum { N = 8 };
    for (int a = 0; a < N; a++)
        for (int b = 0; b < N; b++) {
            double u[4] = {a, a + 1, a + 1, a}, v[4] = {b, b, b + 1, b + 1};
            vec3 n[4], c[4];
            pt p[4];
            for (int k = 0; k < 4; k++) {
                n[k] = normal_at(PI * (u[k] / N - 0.5), PI * (v[k] / N - 0.5));
                c[k] = light(n[k]);
                p[k] = fixed(80 + R * n[k].x, 80 - R * n[k].y);
            }
            int tri[2][3] = {{0, 1, 2}, {0, 2, 3}};
            for (int t = 0; t < 2; t++) {
                int x = tri[t][0], y = tri[t][1], z = tri[t][2];
                if (edge(p[x], p[y], p[z]) < 0) {
                    int s = y;
                    y = z, z = s;
                }
                double area = (double)edge(p[x], p[y], p[z]);
                if (area == 0) continue;  // a cell squeezed to a line at the pole
                for (int j = 0; j < H; j++)
                    for (int i = 0; i < W / 2; i++) {
                        pt q = centre(i, j);
                        if (!inside(p[x], p[y], p[z], q, 1)) continue;
                        double l0 = edge(p[y], p[z], q) / area, l1 = edge(p[z], p[x], q) / area;
                        put(i, j, add(add(mul(c[x], l0), mul(c[y], l1)),
                                      mul(c[z], 1 - l0 - l1)));
                    }
            }
        }
    // per pixel: the normal of the sphere under each pixel centre
    for (int j = 0; j < H; j++)
        for (int i = W / 2; i < W; i++) {
            double x = (i + 0.5 - 240) / R, y = (80 - (j + 0.5)) / R;
            if (x * x + y * y < 1) put(i, j, light(v3(x, y, sqrt(1 - x * x - y * y))));
        }
    int gi = 0, gj = 0, pi = 0, pj = 0;
    double g = peak(0, W / 2, &gi, &gj), p = peak(W / 2, W, &pi, &pj);
    printf("Gouraud:   brightest pixel (%3d, %3d), green %.3f\n", gi, gj, g);
    printf("per pixel: brightest pixel (%3d, %3d), green %.3f\n", pi, pj, p);
    vec3 l = unit(v3(-1, 1, 1)), h = unit(add(l, v3(0, 0, 1)));
    printf("highlight expected where n = (L + V)/|L + V|: pixel (%.1f, %.1f)\n",
           240 + R * h.x - 0.5, 80 - R * h.y - 0.5);
    return write_ppm("../figures/shade.ppm", W, H, &image[0][0][0]) ? 1 : 0;
}
