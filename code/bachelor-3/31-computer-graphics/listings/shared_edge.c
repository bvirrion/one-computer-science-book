// shared_edge.c -- two triangles sharing an edge, both with their vertices on pixel
// centres, drawn with the naive test and with the top-left rule. Each pixel shows
// which triangle drew it: 1, 2, X for both, . for neither.
#include <stdio.h>

#include "raster.h"

int main(void) {
    pt p = centre(1, 1), q = centre(10, 1), r = centre(10, 7), s = centre(1, 7);
    for (int rule = 0; rule <= 1; rule++) {
        int both = 0, none = 0;
        printf("%s\n", rule ? "top-left rule:" : "naive test, w >= 0:");
        for (int j = 0; j < 9; j++) {
            for (int i = 0; i < 12; i++) {
                pt c = centre(i, j);
                int one = inside(p, q, r, c, rule), two = inside(p, r, s, c, rule);
                int square = i >= 1 && i < 10 && j >= 1 && j < 7;  // half-open square
                both += one && two, none += square && !one && !two;
                putchar(one && two ? 'X' : one ? '1' : two ? '2' : '.');
            }
            putchar('\n');
        }
        printf("drawn twice: %d, square pixels missed: %d\n", both, none);
    }
    return 0;
}
