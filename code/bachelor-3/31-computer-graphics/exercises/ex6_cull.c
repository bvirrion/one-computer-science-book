// Exercise 6: back-face culling. The cube's 12 triangles are listed counterclockwise
// seen from outside. A face turned towards the camera is still seen counterclockwise on
// the screen; with y pointing down, edge(a, b, c) is then negative. A back face is seen
// from behind, clockwise, with edge(a, b, c) > 0.
#include <stdio.h>

#include "raster.h"
#include "vec.h"

#define PI 3.14159265358979323846

static const int FACES[6][4] = {  // corners i = x + 2y + 4z of a cube, (x, y, z) in {0, 1}
    {0, 2, 3, 1}, {4, 5, 7, 6}, {0, 1, 5, 4}, {2, 6, 7, 3}, {0, 4, 6, 2}, {1, 3, 7, 5},
};

int front_facing(pt a, pt b, pt c) { return edge(a, b, c) < 0; }

int visible_triangles(mat4 mvp, int cull) {
    pt screen[8];
    for (int i = 0; i < 8; i++) {
        vec4 c = apply(mvp, (vec4){i & 1 ? 1 : -1, i & 2 ? 1 : -1, i & 4 ? 1 : -1, 1});
        screen[i] = fixed((c.x / c.w + 1) / 2 * 320, (1 - c.y / c.w) / 2 * 240);
    }
    int drawn = 0;
    for (int f = 0; f < 6; f++)
        for (int t = 0; t < 2; t++) {
            pt a = screen[FACES[f][0]], b = screen[FACES[f][1 + t]],
               c = screen[FACES[f][2 + t]];
            if (!cull || front_facing(a, b, c)) drawn++;
        }
    return drawn;
}

#ifndef NO_MAIN
int main(void) {
    mat4 model = matmul(translate(0, 0, -6), matmul(rotate_y(PI / 6), rotate_x(PI / 9)));
    mat4 mvp = matmul(perspective(PI / 3, 4.0 / 3.0, 1, 20), model);
    printf("triangles sent: %d, after culling: %d\n", visible_triangles(mvp, 0),
           visible_triangles(mvp, 1));
    return 0;
}
#endif
