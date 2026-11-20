// raster.h -- edge functions and the top-left fill rule, in fixed point (header only).
// Coordinates are integers in 1/16 of a pixel, y pointing down; the centre of pixel
// (i, j) is (16i + 8, 16j + 8). Exact integers make "on the edge" an exact test.
#ifndef RASTER_H
#define RASTER_H
#include <math.h>
#include <stdbool.h>

#define SUB 16

typedef struct { long x, y; } pt;

static inline pt fixed(double x, double y) {  // pixels to 1/16 pixel, rounded
    return (pt){lround(x * SUB), lround(y * SUB)};
}
static inline pt centre(int i, int j) { return (pt){SUB * i + SUB / 2, SUB * j + SUB / 2}; }

// Twice the signed area of (a, b, p): positive when p is to the right of a -> b on a
// screen whose y points down, that is inside a triangle listed clockwise.
static inline long edge(pt a, pt b, pt p) {
    return (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x);
}

// For a clockwise triangle: a top edge is horizontal with the inside below it (it runs
// to the right); a left edge runs up the screen.
static inline bool top_left(pt a, pt b) {
    return (a.y == b.y && b.x > a.x) || b.y < a.y;
}

// Is p drawn as part of the triangle (a, b, c), already put in clockwise order?
// rule 1: the top-left rule; rule 0: the naive test, every point with w >= 0.
static inline bool inside(pt a, pt b, pt c, pt p, int rule) {
    long w[3] = {edge(a, b, p), edge(b, c, p), edge(c, a, p)};
    pt from[3] = {a, b, c}, to[3] = {b, c, a};
    for (int k = 0; k < 3; k++) {
        if (w[k] < 0) return false;
        if (w[k] == 0 && rule == 1 && !top_left(from[k], to[k])) return false;
    }
    return true;
}

static inline void clockwise(pt *a, pt *b, pt *c) {  // swap two vertices if needed
    if (edge(*a, *b, *c) < 0) {
        pt t = *b;
        *b = *c, *c = t;
    }
}
#endif
