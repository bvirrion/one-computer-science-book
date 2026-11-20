// mesh.c -- the weekend problem. Part II: lattice triangles (vertices on pixel centres)
// against Pick's theorem. Part III: meshes covering a 64x48 image, every pixel counted
// with the top-left rule and with the naive test w >= 0: overlaps and gaps.
#include <stdio.h>
#include <stdlib.h>

#include "raster.h"

#define W 64
#define H 48

static unsigned long long state;
static int rnd(int n) {  // a small fixed generator, so that every run is the same
    state = state * 6364136223846793005ULL + 1442695040888963407ULL;
    return (int)((state >> 33) % (unsigned long long)n);
}

static int count[W][H];

static void draw(pt a, pt b, pt c, int rule) {
    clockwise(&a, &b, &c);
    for (int i = 0; i < W; i++)
        for (int j = 0; j < H; j++) count[i][j] += inside(a, b, c, centre(i, j), rule);
}

static void pick(void) {
    printf("lattice triangle             area  interior  boundary  Pick  naive  top-left\n");
    state = 7;
    for (int t = 0; t < 6; t++) {
        pt v[3];
        for (int k = 0; k < 3; k++) v[k] = centre(rnd(24), rnd(18));
        clockwise(&v[0], &v[1], &v[2]);
        long twice = edge(v[0], v[1], v[2]) / (SUB * SUB);
        int interior = 0, boundary = 0, naive = 0, tl = 0;
        for (int i = 0; i < W; i++)
            for (int j = 0; j < H; j++) {
                pt p = centre(i, j);
                int in0 = inside(v[0], v[1], v[2], p, 0);
                int strict = edge(v[0], v[1], p) > 0 && edge(v[1], v[2], p) > 0 &&
                             edge(v[2], v[0], p) > 0;
                interior += strict, boundary += in0 && !strict;
                naive += in0, tl += inside(v[0], v[1], v[2], p, 1);
            }
        printf("(%2ld,%2ld) (%2ld,%2ld) (%2ld,%2ld)  %5.1f  %8d  %8d  %4.1f  %5d  %8d\n",
               v[0].x / SUB, v[0].y / SUB, v[1].x / SUB, v[1].y / SUB, v[2].x / SUB,
               v[2].y / SUB, twice / 2.0, interior, boundary, interior + boundary / 2.0 - 1,
               naive, tl);
    }
}

static void meshes(void) {
    printf("mesh  cells  triangles  rule      drawn  overlap  never\n");
    for (int seed = 1; seed <= 5; seed++) {
        int gx = 4 + seed, gy = 3 + seed;  // vertices on a jittered gx x gy grid of cells
        pt v[16][16];
        state = (unsigned long long)seed;
        for (int i = 0; i <= gx; i++)
            for (int j = 0; j <= gy; j++) {
                long x = (long)SUB * W * i / gx, y = (long)SUB * H * j / gy;
                if (i > 0 && i < gx && j > 0 && j < gy) {
                    if (rnd(3) == 0) {  // on a pixel centre: many samples on edges
                        x = x / SUB * SUB + SUB / 2, y = y / SUB * SUB + SUB / 2;
                    } else {
                        x += rnd(SUB * 5) - SUB * 5 / 2, y += rnd(SUB * 5) - SUB * 5 / 2;
                    }
                }
                v[i][j] = (pt){x, y};
            }
        int diagonal[16][16];
        for (int i = 0; i < gx; i++)
            for (int j = 0; j < gy; j++) diagonal[i][j] = rnd(2);
        for (int rule = 1; rule >= 0; rule--) {
            for (int i = 0; i < W; i++)
                for (int j = 0; j < H; j++) count[i][j] = 0;
            for (int i = 0; i < gx; i++)
                for (int j = 0; j < gy; j++) {
                    pt p = v[i][j], q = v[i + 1][j], r = v[i + 1][j + 1], s = v[i][j + 1];
                    if (diagonal[i][j]) {
                        draw(p, q, r, rule), draw(p, r, s, rule);
                    } else {
                        draw(p, q, s, rule), draw(q, r, s, rule);
                    }
                }
            int drawn = 0, overlap = 0, never = 0;
            for (int i = 0; i < W; i++)
                for (int j = 0; j < H; j++) {
                    drawn += count[i][j], overlap += count[i][j] > 1;
                    never += count[i][j] == 0;
                }
            printf("%4d  %5d  %9d  %-8s  %5d  %7d  %5d\n", seed, gx * gy, 2 * gx * gy,
                   rule ? "top-left" : "w >= 0", drawn, overlap, never);
        }
    }
}

int main(void) {
    pick();
    meshes();
    return 0;
}
