// ppm.h -- write an image as a binary PPM file (header only): "P6", width, height,
// 255, then three bytes per pixel, row by row from the top.
#ifndef PPM_H
#define PPM_H
#include <math.h>
#include <stdio.h>

static inline unsigned char byte(double v) {  // linear light in [0, 1] to sRGB-like gamma
    v = v < 0 ? 0 : v > 1 ? 1 : v;
    return (unsigned char)lround(255 * pow(v, 1 / 2.2));
}

static inline int write_ppm(const char *path, int w, int h, const double *rgb) {
    FILE *f = fopen(path, "wb");
    if (!f) return -1;
    fprintf(f, "P6\n%d %d\n255\n", w, h);
    for (long i = 0; i < 3L * w * h; i++) fputc(byte(rgb[i]), f);
    return fclose(f);
}
#endif
