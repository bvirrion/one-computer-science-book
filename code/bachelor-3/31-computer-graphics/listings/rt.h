// rt.h -- the ray tracer's scene and tracing (header only): three spheres on a
// chequered floor, one point light. trace() follows a ray, sends a shadow ray to the
// light, and, if depth allows, a reflected ray.
#ifndef RT_H
#define RT_H
#include "vec.h"

typedef struct { vec3 centre; double radius; vec3 colour; double mirror; } sphere;

static sphere scene[3] = {
    {{-1.3, -0.2, -5.0}, 0.8, {0.80, 0.18, 0.12}, 0.3},
    {{0.6, -0.45, -4.0}, 0.55, {0.15, 0.55, 0.20}, 0.3},
    {{0.9, 0.5, -6.5}, 1.5, {0.20, 0.30, 0.80}, 0.3},
};
static const double FLOOR_Y = -1.0;
static const vec3 LIGHT = {-4, 5, 1};

// Rays traced, and where they end: ends[0] the sky, ends[1..3] a sphere, ends[4] the floor.
typedef struct { long primary, shadow, reflected, ends[5]; } counts;

// Nearest t > 1e-9 where origin + t d meets the sphere (|d| = 1), or -1.
static double hit_sphere(sphere s, vec3 o, vec3 d) {
    vec3 oc = sub(o, s.centre);
    double b = dot(oc, d), c = dot(oc, oc) - s.radius * s.radius, disc = b * b - c;
    if (disc < 0) return -1;
    double t = -b - sqrt(disc);
    if (t > 1e-9) return t;
    t = -b + sqrt(disc);
    return t > 1e-9 ? t : -1;
}

static double hit_floor(vec3 o, vec3 d) {  // the plane y = FLOOR_Y
    if (fabs(d.y) < 1e-12) return -1;
    double t = (FLOOR_Y - o.y) / d.y;
    return t > 1e-9 ? t : -1;
}

// The nearest hit: returns t, sets *what to 0..2 for a sphere, 3 for the floor.
static double nearest(vec3 o, vec3 d, int *what) {
    double best = -1;
    *what = -1;
    for (int k = 0; k < 3; k++) {
        double t = hit_sphere(scene[k], o, d);
        if (t > 0 && (best < 0 || t < best)) best = t, *what = k;
    }
    double t = hit_floor(o, d);
    if (t > 0 && (best < 0 || t < best)) best = t, *what = 3;
    return best;
}

static vec3 trace(vec3 o, vec3 d, int depth, counts *n) {
    int what;
    double t = nearest(o, d, &what);
    n->ends[what + 1]++;
    if (t < 0) return v3(0.75, 0.85, 1.0);  // the sky
    vec3 p = add(o, mul(d, t)), normal, colour;
    double mirror;
    if (what == 3) {
        normal = v3(0, 1, 0), mirror = 0;
        int check = ((long)floor(p.x) + (long)floor(p.z)) & 1;
        colour = check ? v3(0.85, 0.85, 0.85) : v3(0.35, 0.35, 0.35);
    } else {
        normal = unit(sub(p, scene[what].centre));
        colour = scene[what].colour, mirror = scene[what].mirror;
    }
    vec3 to_light = sub(LIGHT, p);
    double dist = sqrt(dot(to_light, to_light));
    vec3 l = mul(to_light, 1 / dist);
    vec3 start = add(p, mul(normal, 1e-6));  // just off the surface
    int blocker;
    n->shadow++;
    double tb = nearest(start, l, &blocker);
    int lit = !(tb > 0 && tb < dist && blocker != 3);
    double diffuse = lit && dot(normal, l) > 0 ? dot(normal, l) : 0;
    vec3 c = mul(colour, 0.1 + 0.9 * diffuse);
    if (depth > 0 && mirror > 0) {
        n->reflected++;
        vec3 r = sub(d, mul(normal, 2 * dot(d, normal)));
        c = add(mul(c, 1 - mirror), mul(trace(start, r, depth - 1, n), mirror));
    }
    return c;
}
#endif
