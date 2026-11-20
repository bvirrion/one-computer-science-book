// raster.c -- one triangle rasterised into a 32x24 grid of pixels, printed as text:
// a pixel is drawn when its centre is inside, by the three edge functions.
#include <stdio.h>

#include "raster.h"

int main(void) {
    pt a = fixed(3.2, 2.5), b = fixed(28.7, 9.1), c = fixed(9.4, 21.8);
    clockwise(&a, &b, &c);
    int drawn = 0;
    for (int j = 0; j < 24; j++) {
        for (int i = 0; i < 32; i++) {
            int in = inside(a, b, c, centre(i, j), 1);
            drawn += in;
            putchar(in ? '#' : '.');
        }
        putchar('\n');
    }
    double area = edge(a, b, c) / (2.0 * SUB * SUB);
    printf("%d pixels drawn, triangle area %.2f pixels\n", drawn, area);
    return 0;
}
