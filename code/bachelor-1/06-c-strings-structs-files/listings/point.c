// point.c: structures, typedef, designated initialisers, . and ->.
#include <stdio.h>

typedef struct {
    double x, y;
} point;

struct station {
    char name[12];
    point where;
    int altitude;
};

void move_copy(point p) { p.x += 1.0; }                 // changes a copy
void move(point *p) { p->x += 1.0; }                    // changes the caller's point

int main(void)
{
    struct station h = {.name = "Hilltop", .altitude = 212, .where = {.x = 3.5, .y = 7.0}};
    struct station r = {.name = "Riverside"};           // the other fields are zero
    struct station *s = &h;
    printf("%s at (%.1f, %.1f), %d m\n", s->name, s->where.x, s->where.y, s->altitude);
    printf("%s at (%.1f, %.1f), %d m\n", r.name, r.where.x, r.where.y, r.altitude);
    move_copy(h.where);
    printf("after move_copy: x = %.1f\n", h.where.x);
    move(&h.where);
    printf("after move:      x = %.1f\n", h.where.x);
    r = h;                                              // assignment copies every field
    r.name[0] = 'X';
    printf("%s and %s\n", h.name, r.name);
    return 0;
}
