// vec.h -- vectors and 4x4 matrices for the chapter's programs (header only).
#ifndef VEC_H
#define VEC_H
#include <math.h>

typedef struct { double x, y, z; } vec3;
typedef struct { double x, y, z, w; } vec4;
typedef struct { double m[4][4]; } mat4;  // m[row][column]; points are columns

static inline vec3 v3(double x, double y, double z) { return (vec3){x, y, z}; }
static inline vec3 add(vec3 a, vec3 b) { return v3(a.x + b.x, a.y + b.y, a.z + b.z); }
static inline vec3 sub(vec3 a, vec3 b) { return v3(a.x - b.x, a.y - b.y, a.z - b.z); }
static inline vec3 mul(vec3 a, double s) { return v3(a.x * s, a.y * s, a.z * s); }
static inline double dot(vec3 a, vec3 b) { return a.x * b.x + a.y * b.y + a.z * b.z; }
static inline vec3 cross(vec3 a, vec3 b) {
    return v3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
}
static inline vec3 unit(vec3 a) { return mul(a, 1.0 / sqrt(dot(a, a))); }

static inline mat4 identity(void) {
    mat4 r = {{{0}}};
    for (int i = 0; i < 4; i++) r.m[i][i] = 1;
    return r;
}
static inline mat4 matmul(mat4 a, mat4 b) {  // a * b: apply b first, then a
    mat4 r = {{{0}}};
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            for (int k = 0; k < 4; k++) r.m[i][j] += a.m[i][k] * b.m[k][j];
    return r;
}
static inline vec4 apply(mat4 a, vec4 p) {
    double in[4] = {p.x, p.y, p.z, p.w}, out[4] = {0};
    for (int i = 0; i < 4; i++)
        for (int k = 0; k < 4; k++) out[i] += a.m[i][k] * in[k];
    return (vec4){out[0], out[1], out[2], out[3]};
}
static inline mat4 translate(double tx, double ty, double tz) {
    mat4 r = identity();
    r.m[0][3] = tx, r.m[1][3] = ty, r.m[2][3] = tz;
    return r;
}
static inline mat4 rotate_y(double a) {  // a in radians, counterclockwise seen from +y
    mat4 r = identity();
    r.m[0][0] = cos(a), r.m[0][2] = sin(a), r.m[2][0] = -sin(a), r.m[2][2] = cos(a);
    return r;
}
static inline mat4 rotate_x(double a) {
    mat4 r = identity();
    r.m[1][1] = cos(a), r.m[1][2] = -sin(a), r.m[2][1] = sin(a), r.m[2][2] = cos(a);
    return r;
}
// Perspective projection: camera at the origin looking down -z, vertical field of view
// fovy, z = -near and z = -far mapped to depths -1 and +1 after division by w = -z.
static inline mat4 perspective(double fovy, double aspect, double near, double far) {
    double f = 1.0 / tan(fovy / 2);
    mat4 r = {{{0}}};
    r.m[0][0] = f / aspect;
    r.m[1][1] = f;
    r.m[2][2] = (far + near) / (near - far);
    r.m[2][3] = 2 * far * near / (near - far);
    r.m[3][2] = -1;
    return r;
}
#endif
