// raster_test.c -- the chapter's geometry, checked: the fill rule, Pick's theorem,
// the perspective matrix, ray intersections and back-face culling.
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#define NO_MAIN
#include "../exercises/ex12_reflect.c"
#include "../exercises/ex6_cull.c"

#define PI 3.14159265358979323846

static unsigned long long s = 31;
static long rnd(long n) {
    s = s * 6364136223846793005ULL + 1442695040888963407ULL;
    return (long)((s >> 33) % (unsigned long long)n);
}

static void fill_rule(void) {  // every split of a square, and random shared edges
    for (int trial = 0; trial < 2000; trial++) {
        pt p = {rnd(40 * SUB), rnd(40 * SUB)}, q = {rnd(40 * SUB), rnd(40 * SUB)};
        pt r = {rnd(40 * SUB), rnd(40 * SUB)}, u = {rnd(40 * SUB), rnd(40 * SUB)};
        if (trial % 2) p = centre(rnd(40), rnd(40)), q = centre(rnd(40), rnd(40));
        // (p, q, r) and (q, p, u) share the edge pq; r and u on opposite sides
        long sr = edge(p, q, r), su = edge(p, q, u);
        if (sr == 0 || su == 0 || (sr > 0) == (su > 0)) continue;
        pt a1 = p, b1 = q, c1 = r, a2 = q, b2 = p, c2 = u;
        clockwise(&a1, &b1, &c1), clockwise(&a2, &b2, &c2);
        for (int i = 0; i < 40; i++)
            for (int j = 0; j < 40; j++) {
                pt c = centre(i, j);
                int one = inside(a1, b1, c1, c, 1), two = inside(a2, b2, c2, c, 1);
                assert(!(one && two));  // never drawn twice
                // a centre strictly inside the quadrilateral's shared edge is drawn once
                if (edge(p, q, c) == 0) {
                    long t1 = (c.x - p.x) * (q.x - p.x) + (c.y - p.y) * (q.y - p.y);
                    long len = (q.x - p.x) * (q.x - p.x) + (q.y - p.y) * (q.y - p.y);
                    if (t1 > 0 && t1 < len) assert(one || two);
                }
            }
    }
}

static void pick(void) {  // 2A = 2I + B - 2 on random lattice triangles
    for (int trial = 0; trial < 300; trial++) {
        pt a = centre(rnd(30), rnd(30)), b = centre(rnd(30), rnd(30)), c = centre(rnd(30), rnd(30));
        clockwise(&a, &b, &c);
        long twice = edge(a, b, c) / (SUB * SUB);
        if (twice == 0) continue;
        long in = 0, on = 0;
        for (int i = 0; i < 30; i++)
            for (int j = 0; j < 30; j++) {
                pt p = centre(i, j);
                long e0 = edge(a, b, p), e1 = edge(b, c, p), e2 = edge(c, a, p);
                if (e0 > 0 && e1 > 0 && e2 > 0) in++;
                else if (e0 >= 0 && e1 >= 0 && e2 >= 0) on++;
            }
        assert(twice == 2 * in + on - 2);
    }
}

static void problem(void) {
    // Part I: the 9 x 6 square of shared_edge.c, Pick: 40 interior, 30 boundary, area 54
    pt p = centre(1, 1), q = centre(10, 1), r = centre(10, 7), u = centre(1, 7);
    int drawn = 0, interior = 0, boundary = 0;
    for (int i = 0; i < 12; i++)
        for (int j = 0; j < 9; j++) {
            pt c = centre(i, j);
            drawn += inside(p, q, r, c, 1) + inside(p, r, u, c, 1);
            int in = i >= 1 && i <= 10 && j >= 1 && j <= 7, strict = i > 1 && i < 10 && j > 1 && j < 7;
            interior += strict, boundary += in && !strict;
        }
    assert(drawn == 54 && interior == 40 && boundary == 30 && interior + boundary / 2 - 1 == 54);
    // Part II, row 2: (12, 10), (22, 13), (3, 13): 20 of its 23 boundary points on the
    // bottom edge, 2 inside the left edge; the top-left rule keeps 18 + 2 = 20
    pt a = centre(12, 10), b = centre(22, 13), c = centre(3, 13);
    int bottom = 0, left = 0, kept = 0;
    for (int i = 0; i < 30; i++)
        for (int j = 0; j < 20; j++) {
            pt x = centre(i, j);
            kept += inside(a, b, c, x, 1);
            bottom += edge(b, c, x) == 0 && i >= 3 && i <= 22;
            left += edge(c, a, x) == 0 && i > 3 && i < 12;
        }
    assert(edge(a, b, c) > 0 && bottom == 20 && left == 2 && kept == 20);
    assert(top_left(c, a) && !top_left(a, b) && !top_left(b, c));
}

static void projection(void) {  // near plane to depth -1, far plane to +1, w = -z
    mat4 p = perspective(PI / 3, 4.0 / 3.0, 1, 20);
    vec4 n = apply(p, (vec4){0, 0, -1, 1}), f = apply(p, (vec4){0, 0, -20, 1});
    assert(fabs(n.z / n.w + 1) < 1e-12 && fabs(f.z / f.w - 1) < 1e-12 && f.w == 20);
    vec4 top = apply(p, (vec4){0, tan(PI / 6) * 5, -5, 1});  // on the top plane: y = 1
    assert(fabs(top.y / top.w - 1) < 1e-12);
}

static void rays(void) {
    sphere unit_s = {{0, 0, -5}, 1, {1, 1, 1}, 0};
    assert(fabs(hit_sphere(unit_s, v3(0, 0, 0), v3(0, 0, -1)) - 4) < 1e-12);
    assert(hit_sphere(unit_s, v3(0, 0, 0), unit(v3(1, 0, -2))) < 0);  // misses
    assert(fabs(hit_sphere(unit_s, v3(0, 0, -5), v3(1, 0, 0)) - 1) < 1e-12);  // from inside
    assert(fabs(hit_floor(v3(0, 1, 0), unit(v3(0, -1, -1))) - 2 * sqrt(2)) < 1e-12);
    assert(hit_floor(v3(0, 1, 0), v3(0, 1, 0)) < 0);
    double edge_angle = asin(0.2);  // Exercise 9: rays from the origin graze the sphere here
    assert(hit_sphere(unit_s, v3(0, 0, 0), v3(sin(edge_angle - 1e-6), 0, -cos(edge_angle - 1e-6))) > 0);
    assert(hit_sphere(unit_s, v3(0, 0, 0), v3(sin(edge_angle + 1e-6), 0, -cos(edge_angle + 1e-6))) < 0);
    assert(fabs(edge_angle * 180 / PI - 11.54) < 0.005);
    counts n = {0};
    vec3 sky = trace(v3(0, 0, 0), v3(0, 1, 0), 3, &n);
    assert(sky.x == 0.75 && n.ends[0] == 1 && n.shadow == 0);
    trace(v3(0, 0, 0), unit(v3(-1.3, -0.2, -5.0)), 0, &n);  // at the red sphere's centre
    assert(n.ends[1] == 1 && n.shadow == 1 && n.reflected == 0);
}

static void culling(void) {  // the kept triangles are exactly those facing the camera
    for (int k = 0; k < 24; k++) {
        double ay = k * PI / 12, ax = (k % 5) * PI / 10;
        mat4 model = matmul(translate(0, 0, -6), matmul(rotate_y(ay), rotate_x(ax)));
        mat4 mvp = matmul(perspective(PI / 3, 4.0 / 3.0, 1, 20), model);
        int facing = 0;
        for (int f = 0; f < 6; f++) {  // face normal in camera space vs the camera ray
            vec4 n4 = {0, 0, 0, 0}, c4 = {0, 0, 0, 1};
            if (f < 2) n4.z = f ? 1 : -1, c4.z = n4.z;
            else if (f < 4) n4.y = f == 3 ? 1 : -1, c4.y = n4.y;
            else n4.x = f == 5 ? 1 : -1, c4.x = n4.x;
            vec4 n = apply(model, n4), c = apply(model, c4);
            facing += n.x * c.x + n.y * c.y + n.z * c.z < 0;
        }
        assert(visible_triangles(mvp, 0) == 12 && visible_triangles(mvp, 1) == 2 * facing);
    }
}

static void exercises(void) {
    // Exercise 1: a translation moves points (w = 1), not directions (w = 0)
    vec4 pt1 = apply(translate(2, 0, 0), (vec4){1, 1, 1, 1});
    vec4 dir = apply(translate(2, 0, 0), (vec4){1, 1, 1, 0});
    vec4 turned = apply(rotate_y(PI / 2), (vec4){1, 0, 0, 1});
    assert(pt1.x == 3 && dir.x == 1 && fabs(turned.x) < 1e-12 && fabs(turned.z + 1) < 1e-12);
    // Exercise 3: the three edge functions at (2, 3) and their sum, twice the area
    pt ta = fixed(0, 0), tb = fixed(8, 0), tc = fixed(0, 8), tp = fixed(2, 3);
    long s2 = SUB * SUB;
    assert(edge(ta, tb, tp) == 24 * s2 && edge(tb, tc, tp) == 24 * s2 && edge(tc, ta, tp) == 16 * s2);
    assert(edge(ta, tb, tc) == 64 * s2);
    // Exercise 4: (1, 1), (7, 2), (2, 6): 15 pixels for an area of 14.5; centre (1, 3) on an edge
    pt ea = fixed(1, 1), eb = fixed(7, 2), ec = fixed(2, 6);
    int drawn = 0;
    for (int i = 0; i < 8; i++)
        for (int j = 0; j < 7; j++) drawn += inside(ea, eb, ec, centre(i, j), 1);
    assert(edge(ea, eb, ec) == 29 * s2 && drawn == 15);
    assert(edge(ec, ea, centre(1, 3)) == 0 && top_left(ec, ea) && inside(ea, eb, ec, centre(1, 3), 1));
    // Exercise 8: the highlight, where n is the halfway vector of L and V
    vec3 h = unit(add(unit(v3(-1, 1, 1)), v3(0, 0, 1)));
    assert(fabs(h.x + 0.3251) < 1e-4 && fabs(h.z - 0.8881) < 1e-4);
    assert(fabs(240 + 70 * h.x - 0.5 - 216.75) < 0.01 && fabs(80 - 70 * h.y - 0.5 - 56.75) < 0.01);
    // Exercise 2: two points on one line of sight have the same NDC y, sqrt(3)/2
    mat4 p = perspective(PI / 3, 4.0 / 3.0, 1, 20);
    vec4 a = apply(p, (vec4){0, 1, -2, 1}), b = apply(p, (vec4){0, 2, -4, 1});
    assert(fabs(a.y / a.w - sqrt(3) / 2) < 1e-12 && fabs(b.y / b.w - sqrt(3) / 2) < 1e-12);
    // Exercise 5: translating first, the centre circles the camera
    vec4 o = {0, 0, 0, 1};
    vec4 bug = apply(matmul(rotate_y(PI / 4), translate(0, 0, -6)), o);
    vec4 fix = apply(matmul(translate(0, 0, -6), rotate_y(PI / 4)), o);
    assert(fabs(bug.x + 3 * sqrt(2)) < 1e-12 && fabs(bug.z + 3 * sqrt(2)) < 1e-12);
    assert(fabs(fix.x) < 1e-12 && fabs(fix.z + 6) < 1e-12);
    // Exercise 7: NDC depth (21 - 40/d)/19 at the distances 1, 2, 10, 20
    double d[4] = {1, 2, 10, 20}, want[4] = {-1, 1.0 / 19, 17.0 / 19, 1};
    for (int k = 0; k < 4; k++) {
        vec4 c = apply(p, (vec4){0, 0, -d[k], 1});
        assert(fabs(c.z / c.w - want[k]) < 1e-12);
    }
    // Exercise 12: the ray counts for the depth limits 0 to 4
    long refl[5] = {0, 12421, 13333, 13478, 13498}, shad[5] = {45170, 50881, 51343, 51422, 51435};
    for (int limit = 0; limit <= 4; limit++) {
        counts n = render(limit, NULL);
        assert(n.primary == 76800 && n.reflected == refl[limit] && n.shadow == shad[limit]);
        if (limit == 1)  // every primary ray that ends on a sphere is reflected once
            assert(n.reflected == 3686 + 2661 + 6074);
    }
}

int main(void) {
    exercises();
    problem();
    fill_rule();
    pick();
    projection();
    rays();
    culling();
    printf("raster_test: all passed\n");
    return 0;
}
